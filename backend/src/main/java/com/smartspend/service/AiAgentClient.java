package com.smartspend.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.List;
import java.util.Map;

@Service
@Slf4j
public class AiAgentClient {

    private final WebClient webClient;

    public AiAgentClient(@Qualifier("aiAgentWebClient") WebClient webClient) {
        this.webClient = webClient;
    }

    public String getFinancialAdvice(Long userId, Map<String, Object> financialData) {
        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> response = webClient.post()
                    .uri("/api/advice")
                    .bodyValue(Map.of(
                            "user_id", userId,
                            "financial_data", financialData
                    ))
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

            if (response != null && response.containsKey("advice")) {
                return (String) response.get("advice");
            }
        } catch (Exception e) {
            log.error("Error calling AI agent for advice: {}", e.getMessage());
        }
        return "Unable to generate advice at this time.";
    }

    public Map<String, Object> getAdvice(Map<String, Object> spendingSummary) {
        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> response = webClient.post()
                    .uri("/api/advice")
                    .bodyValue(spendingSummary)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

            return response != null ? response : getDefaultAdvice();
        } catch (Exception e) {
            log.error("Error calling AI agent for advice: {}", e.getMessage());
            return getDefaultAdvice();
        }
    }

    private Map<String, Object> getDefaultAdvice() {
        return Map.of(
            "summary", "Unable to generate advice at this time.",
            "recommendations", List.of("Track your expenses regularly", "Set a monthly budget"),
            "savingsOpportunities", List.of()
        );
    }

    public Map<String, Object> analyzeSpendingPatterns(Long userId, List<Map<String, Object>> transactions) {
        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> response = webClient.post()
                    .uri("/api/patterns")
                    .bodyValue(Map.of(
                            "user_id", userId,
                            "transactions", transactions
                    ))
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

            return response != null ? response : Map.of("error", "No response");
        } catch (Exception e) {
            log.error("Error calling AI agent for pattern analysis: {}", e.getMessage());
            return Map.of("error", "Unable to analyze patterns");
        }
    }

    public Map<String, Object> getPatterns(Map<String, Object> transactionData) {
        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> response = webClient.post()
                    .uri("/api/patterns")
                    .bodyValue(transactionData)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

            return response != null ? response : Map.of("patterns", List.of());
        } catch (Exception e) {
            log.error("Error calling AI agent for pattern analysis: {}", e.getMessage());
            return Map.of("patterns", List.of(), "message", "Unable to analyze patterns at this time.");
        }
    }

    public String chat(Long userId, String message, Map<String, Object> context) {
        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> response = webClient.post()
                    .uri("/api/chat")
                    .bodyValue(Map.of(
                            "user_id", userId,
                            "message", message,
                            "context", context
                    ))
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

            if (response != null && response.containsKey("response")) {
                return (String) response.get("response");
            }
        } catch (Exception e) {
            log.error("Error calling AI agent chat: {}", e.getMessage());
        }
        return "I'm having trouble responding right now. Please try again later.";
    }

    public Map<String, Object> chat(String message, Map<String, Object> context) {
        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> response = webClient.post()
                    .uri("/api/chat")
                    .bodyValue(Map.of(
                            "message", message,
                            "context", context != null ? context : Map.of()
                    ))
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

            return response != null ? response : getDefaultChatResponse();
        } catch (Exception e) {
            log.error("Error calling AI agent chat: {}", e.getMessage());
            return getDefaultChatResponse();
        }
    }

    private Map<String, Object> getDefaultChatResponse() {
        return Map.of(
            "response", "I'm having trouble connecting right now. Please try again later.",
            "suggestions", List.of()
        );
    }
}
