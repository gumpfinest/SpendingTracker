package com.smartspend.controller;

import com.smartspend.entity.Transaction;
import com.smartspend.entity.User;
import com.smartspend.repository.TransactionRepository;
import com.smartspend.repository.UserRepository;
import com.smartspend.service.AiAgentClient;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/ai")
@RequiredArgsConstructor
public class AiController {

    private final AiAgentClient aiAgentClient;
    private final TransactionRepository transactionRepository;
    private final UserRepository userRepository;

    @PostMapping("/advice")
    public ResponseEntity<Map<String, Object>> getAdvice(
            @RequestBody Map<String, Object> spendingSummary,
            @AuthenticationPrincipal UserDetails userDetails) {
        Map<String, Object> advice = aiAgentClient.getAdvice(spendingSummary);
        return ResponseEntity.ok(advice);
    }

    @PostMapping("/chat")
    public ResponseEntity<Map<String, Object>> chat(
            @RequestBody Map<String, Object> request,
            @AuthenticationPrincipal UserDetails userDetails) {
        String message = (String) request.get("message");
        Map<String, Object> context = (Map<String, Object>) request.getOrDefault("context", Map.of());
        
        // Enrich context with user's recent transactions if not provided
        if (!context.containsKey("recentTransactions")) {
            User user = userRepository.findByUsername(userDetails.getUsername())
                    .orElseThrow(() -> new RuntimeException("User not found"));
            List<Transaction> recentTransactions = transactionRepository
                    .findByUserOrderByTransactionDateDesc(user)
                    .stream()
                    .limit(10)
                    .collect(Collectors.toList());
            
            context = Map.of(
                "recentTransactions", recentTransactions.stream()
                    .map(t -> Map.of(
                        "description", t.getDescription(),
                        "amount", t.getAmount(),
                        "category", t.getCategory() != null ? t.getCategory() : "Uncategorized",
                        "type", t.getType().name()
                    ))
                    .collect(Collectors.toList())
            );
        }
        
        Map<String, Object> response = aiAgentClient.chat(message, context);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/patterns")
    public ResponseEntity<Map<String, Object>> getPatterns(
            @AuthenticationPrincipal UserDetails userDetails) {
        User user = userRepository.findByUsername(userDetails.getUsername())
                .orElseThrow(() -> new RuntimeException("User not found"));
        
        LocalDateTime startDate = LocalDateTime.now().minusMonths(3);
        List<Transaction> transactions = transactionRepository
                .findByUserAndTransactionDateBetween(user, startDate, LocalDateTime.now());
        
        Map<String, Object> transactionData = Map.of(
            "transactions", transactions.stream()
                .map(t -> Map.of(
                    "description", t.getDescription(),
                    "amount", t.getAmount(),
                    "category", t.getCategory() != null ? t.getCategory() : "Uncategorized",
                    "type", t.getType().name(),
                    "date", t.getTransactionDate().toString()
                ))
                .collect(Collectors.toList())
        );
        
        Map<String, Object> patterns = aiAgentClient.getPatterns(transactionData);
        return ResponseEntity.ok(patterns);
    }
}
