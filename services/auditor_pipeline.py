"""
Unified Conversation Auditor Pipeline.
Orchestrates ingestion, multilingual identification, relevance tagging,
claim verification, 100-point rubric scoring, and coaching synthesis.
"""
from typing import Dict, List, Any, Optional
from services.language_detector import LanguageDetector
from services.stt_service import TranscriptIngestionService
from services.knowledge_base import ProductKnowledgeBase
from services.relevance_classifier import RelevanceClassifier
from services.claim_verifier import ClaimVerifier
from services.quality_scorer import QualityScorer
from services.coach_generator import CoachGenerator

class ProductGuardAuditorPipeline:
    """
    End-to-end conversation compliance auditor.
    """
    def __init__(self, kb: Optional[ProductKnowledgeBase] = None):
        self.kb = kb or ProductKnowledgeBase()
        self.claim_verifier = ClaimVerifier(self.kb)
        self.coach_generator = CoachGenerator(self.kb)

    def audit_conversation(
        self,
        call_id: str,
        product_id: str,
        provider_name: str,
        raw_transcript: Optional[str] = None,
        structured_segments: Optional[List[Dict[str, Any]]] = None,
        target_report_language: str = "Hinglish"
    ) -> Dict[str, Any]:
        """
        Executes full audit workflow.
        """
        # 1. Ingestion & Segment Extraction
        if structured_segments:
            segments = TranscriptIngestionService.parse_json_transcript(structured_segments)
        elif raw_transcript:
            segments = TranscriptIngestionService.parse_text_transcript(raw_transcript)
        else:
            segments = []

        all_claims = []
        customer_questions = []
        answered_questions = []
        last_question = None

        # 2. Sequential Analysis per Conversational Turn
        for seg in segments:
            role = seg["speaker_role"]
            text = seg["text"]

            if role == "customer":
                # Detect if question
                if "?" in text or any(k in text.lower() for k in ["kya", "kitna", "how", "what", "is it", "can"]):
                    customer_questions.append(text)
                    last_question = text
            else:
                # Role is provider: Extract claims
                claims_in_turn = self.claim_verifier.extract_and_verify(
                    provider_statement=text,
                    product_id=product_id,
                    timestamp=seg.get("start_time", 0.0),
                    segment_id=seg.get("id")
                )
                all_claims.extend(claims_in_turn)

                is_contradicted = any(c["verification_status"] == "contradicted" for c in claims_in_turn)
                is_unsupported = any(c["verification_status"] == "unsupported" for c in claims_in_turn)

                # Classify relevance
                rel_info = RelevanceClassifier.classify_turn(
                    current_text=text,
                    last_customer_question=last_question,
                    is_contradicted=is_contradicted,
                    is_unsupported=is_unsupported
                )

                seg["topic_category"] = rel_info["category"]
                seg["topic_label"] = rel_info["label"]
                seg["is_off_topic"] = rel_info["is_off_topic"]
                seg["relevance_explanation"] = rel_info["explanation"]

                if last_question and not rel_info["is_off_topic"] and rel_info["category"] != "repetition_unnecessary_elaboration":
                    if last_question not in answered_questions:
                        answered_questions.append(last_question)

        # 3. 100-Point Evaluation Scoring
        evaluation = QualityScorer.evaluate(
            segments=segments,
            claims=all_claims,
            customer_questions=customer_questions,
            answered_questions=answered_questions
        )

        # 4. Coaching Report Generation
        report = self.coach_generator.generate_report(
            call_id=call_id,
            product_id=product_id,
            provider_name=provider_name,
            segments=segments,
            claims=all_claims,
            evaluation=evaluation,
            target_language=target_report_language
        )

        return {
            "call_id": call_id,
            "product_id": product_id,
            "provider_name": provider_name,
            "target_language": target_report_language,
            "segments": segments,
            "claims": all_claims,
            "evaluation": evaluation,
            "report": report
        }

    def audit_realtime_turn(
        self,
        product_id: str,
        turn_text: str,
        speaker_role: str = "provider",
        conversation_history: Optional[List[Dict[str, Any]]] = None,
        target_language: str = "Hinglish",
        generate_tts: bool = False
    ) -> Dict[str, Any]:
        """
        Audits a single conversational turn in real-time.
        Returns immediate compliance status, claim checks, alerts, and grounded rewrites.
        """
        history = conversation_history or []
        lang_info = LanguageDetector.detect(turn_text)
        
        # Identify last customer question
        last_question = None
        for prev in reversed(history):
            if prev.get("speaker_role") == "customer" and ("?" in prev.get("text", "") or any(k in prev.get("text", "").lower() for k in ["kya", "kitna", "how", "what", "is it", "can"])):
                last_question = prev.get("text")
                break

        if speaker_role == "customer":
            is_question = "?" in turn_text or any(k in turn_text.lower() for k in ["kya", "kitna", "how", "what", "is it", "can i"])
            return {
                "speaker_role": "customer",
                "text": turn_text,
                "detected_language": lang_info["language"],
                "language_label": lang_info["label"],
                "is_question": is_question,
                "claims": [],
                "alert_type": "INFO",
                "alert_message": "Customer inquiry received." if is_question else "Customer statement recorded.",
                "instant_correction": None,
                "tts_audio": None
            }

        # Role is Provider: Extract claims
        claims = self.claim_verifier.extract_and_verify(
            provider_statement=turn_text,
            product_id=product_id,
            timestamp=float(len(history) * 4.0)
        )

        is_contradicted = any(c["verification_status"] == "contradicted" for c in claims)
        is_unsupported = any(c["verification_status"] == "unsupported" for c in claims)

        rel_info = RelevanceClassifier.classify_turn(
            current_text=turn_text,
            last_customer_question=last_question,
            is_contradicted=is_contradicted,
            is_unsupported=is_unsupported
        )

        # Determine Real-Time Alert Status
        alert_type = "SUCCESS"
        alert_message = "Statement is compliant and verified."
        instant_correction = None

        if is_contradicted:
            alert_type = "CRITICAL"
            contradicted_claim = [c for c in claims if c["verification_status"] == "contradicted"][0]
            alert_message = f"CRITICAL: Statement contradicts approved catalog! {contradicted_claim.get('explanation')}"
            correction = self.coach_generator.generate_corrected_response(
                customer_question=last_question or contradicted_claim.get("claim_text", ""),
                problematic_statement=turn_text,
                product_id=product_id,
                target_language=target_language
            )
            instant_correction = correction["corrected_text"]

        elif is_unsupported:
            alert_type = "WARNING"
            alert_message = "WARNING: Uncataloged claim made without verified source documentation."
            correction = self.coach_generator.generate_corrected_response(
                customer_question=last_question or turn_text,
                problematic_statement=turn_text,
                product_id=product_id,
                target_language=target_language
            )
            instant_correction = correction["corrected_text"]

        elif rel_info["is_off_topic"]:
            alert_type = "WARNING"
            alert_message = "ALERT: Off-topic personal story detected. Pivot back to customer value."
            if last_question:
                correction = self.coach_generator.generate_corrected_response(
                    customer_question=last_question,
                    problematic_statement=turn_text,
                    product_id=product_id,
                    target_language=target_language
                )
                instant_correction = correction["corrected_text"]

        # Optional real-time speech synthesis for instant correction
        tts_audio = None
        if generate_tts and instant_correction:
            from services.audio_service import AudioService
            tts_audio = AudioService.synthesize_speech_wav(instant_correction)

        return {
            "speaker_role": "provider",
            "text": turn_text,
            "detected_language": lang_info["language"],
            "language_label": lang_info["label"],
            "topic_category": rel_info["category"],
            "topic_label": rel_info["label"],
            "is_off_topic": rel_info["is_off_topic"],
            "claims": claims,
            "alert_type": alert_type,
            "alert_message": alert_message,
            "instant_correction": instant_correction,
            "tts_audio": tts_audio
        }
