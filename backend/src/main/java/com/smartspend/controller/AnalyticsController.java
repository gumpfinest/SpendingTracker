package com.smartspend.controller;

import com.smartspend.dto.AnalyticsDTO;
import com.smartspend.entity.User;
import com.smartspend.service.AnalyticsService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/analytics")
@RequiredArgsConstructor
@Tag(name = "Analytics", description = "Financial analytics and insights endpoints")
public class AnalyticsController {

    private final AnalyticsService analyticsService;

    @GetMapping("/dashboard")
    @Operation(summary = "Get dashboard summary with key financial metrics")
    public ResponseEntity<AnalyticsDTO.DashboardSummary> getDashboardSummary(
            @AuthenticationPrincipal User user) {
        return ResponseEntity.ok(analyticsService.getDashboardSummary(user));
    }

    @GetMapping("/forecast")
    @Operation(summary = "Get spending forecast for the next 6 months")
    public ResponseEntity<Map<String, Object>> getSpendingForecast(
            @AuthenticationPrincipal User user) {
        return ResponseEntity.ok(analyticsService.getSpendingForecast(user));
    }

    @GetMapping("/analysis")
    @Operation(summary = "Get detailed spending analysis")
    public ResponseEntity<Map<String, Object>> getSpendingAnalysis(
            @AuthenticationPrincipal User user) {
        return ResponseEntity.ok(analyticsService.getSpendingAnalysis(user));
    }

    @GetMapping("/advice")
    @Operation(summary = "Get AI-powered financial advice")
    public ResponseEntity<Map<String, String>> getAiAdvice(
            @AuthenticationPrincipal User user) {
        String advice = analyticsService.getAiAdvice(user);
        return ResponseEntity.ok(Map.of("advice", advice));
    }

    @PostMapping("/chat")
    @Operation(summary = "Chat with AI financial assistant")
    public ResponseEntity<Map<String, String>> chatWithAi(
            @AuthenticationPrincipal User user,
            @RequestBody Map<String, String> request) {
        String message = request.get("message");
        String response = analyticsService.chatWithAiAgent(user, message);
        return ResponseEntity.ok(Map.of("response", response));
    }
}
