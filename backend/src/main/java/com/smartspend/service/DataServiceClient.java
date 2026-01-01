package com.smartspend.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.List;
import java.util.Map;

@Service
@Slf4j
public class DataServiceClient {

    private final WebClient webClient;

    public DataServiceClient(@Qualifier("dataServiceWebClient") WebClient webClient) {
        this.webClient = webClient;
    }

    public String categorizeTransaction(String description) {
        try {
            Map<String, Object> response = webClient.post()
                    .uri("/api/categorize")
                    .bodyValue(Map.of("description", description))
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

            if (response != null && response.containsKey("category")) {
                return (String) response.get("category");
            }
        } catch (Exception e) {
            log.error("Error calling data service for categorization: {}", e.getMessage());
        }
        return "Uncategorized";
    }

    public Map<String, Object> getSpendingForecast(Long userId, List<Map<String, Object>> transactions) {
        try {
            return webClient.post()
                    .uri("/api/forecast")
                    .bodyValue(Map.of(
                            "user_id", userId,
                            "transactions", transactions
                    ))
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();
        } catch (Exception e) {
            log.error("Error calling data service for forecast: {}", e.getMessage());
            return Map.of("error", "Unable to generate forecast");
        }
    }

    public Map<String, Object> analyzeSpending(Long userId, List<Map<String, Object>> transactions) {
        try {
            return webClient.post()
                    .uri("/api/analyze")
                    .bodyValue(Map.of(
                            "user_id", userId,
                            "transactions", transactions
                    ))
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();
        } catch (Exception e) {
            log.error("Error calling data service for analysis: {}", e.getMessage());
            return Map.of("error", "Unable to analyze spending");
        }
    }
}
