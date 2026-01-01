package com.smartspend.service;

import com.smartspend.dto.AnalyticsDTO;
import com.smartspend.dto.TransactionDTO;
import com.smartspend.entity.Transaction;
import com.smartspend.entity.User;
import com.smartspend.repository.TransactionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.YearMonth;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class AnalyticsService {

    private final TransactionRepository transactionRepository;
    private final DataServiceClient dataServiceClient;
    private final AiAgentClient aiAgentClient;

    public AnalyticsDTO.DashboardSummary getDashboardSummary(User user) {
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime startOfMonth = now.withDayOfMonth(1).withHour(0).withMinute(0).withSecond(0);
        LocalDateTime endOfMonth = YearMonth.from(now).atEndOfMonth().atTime(23, 59, 59);

        // Get monthly income
        BigDecimal monthlyIncome = transactionRepository.sumByUserAndTypeAndDateRange(
                user, Transaction.TransactionType.INCOME, startOfMonth, endOfMonth);

        // Get monthly expenses
        BigDecimal monthlyExpenses = transactionRepository.sumByUserAndTypeAndDateRange(
                user, Transaction.TransactionType.EXPENSE, startOfMonth, endOfMonth);

        // Calculate savings
        BigDecimal monthlySavings = monthlyIncome.subtract(monthlyExpenses);

        // Get spending by category
        Map<String, BigDecimal> spendingByCategory = new HashMap<>();
        List<Object[]> categoryData = transactionRepository.getSpendingByCategory(
                user, startOfMonth, endOfMonth);
        for (Object[] row : categoryData) {
            spendingByCategory.put((String) row[0], (BigDecimal) row[1]);
        }

        // Get recent transactions
        List<TransactionDTO.Response> recentTransactions = transactionRepository
                .findByUserOrderByTransactionDateDesc(user)
                .stream()
                .limit(10)
                .map(TransactionDTO.Response::fromEntity)
                .collect(Collectors.toList());

        // Calculate total balance (simplified - sum of all income minus expenses)
        BigDecimal totalIncome = transactionRepository.sumByUserAndTypeAndDateRange(
                user, Transaction.TransactionType.INCOME, 
                LocalDateTime.of(2000, 1, 1, 0, 0), now);
        BigDecimal totalExpenses = transactionRepository.sumByUserAndTypeAndDateRange(
                user, Transaction.TransactionType.EXPENSE, 
                LocalDateTime.of(2000, 1, 1, 0, 0), now);
        BigDecimal totalBalance = totalIncome.subtract(totalExpenses);

        return AnalyticsDTO.DashboardSummary.builder()
                .totalBalance(totalBalance)
                .monthlyIncome(monthlyIncome)
                .monthlyExpenses(monthlyExpenses)
                .monthlySavings(monthlySavings)
                .spendingByCategory(spendingByCategory)
                .recentTransactions(recentTransactions)
                .build();
    }

    public Map<String, Object> getSpendingForecast(User user) {
        // Get all user transactions
        List<Map<String, Object>> transactions = transactionRepository
                .findByUserOrderByTransactionDateDesc(user)
                .stream()
                .map(this::transactionToMap)
                .collect(Collectors.toList());

        return dataServiceClient.getSpendingForecast(user.getId(), transactions);
    }

    public Map<String, Object> getSpendingAnalysis(User user) {
        List<Map<String, Object>> transactions = transactionRepository
                .findByUserOrderByTransactionDateDesc(user)
                .stream()
                .map(this::transactionToMap)
                .collect(Collectors.toList());

        return dataServiceClient.analyzeSpending(user.getId(), transactions);
    }

    public String getAiAdvice(User user) {
        AnalyticsDTO.DashboardSummary summary = getDashboardSummary(user);
        
        Map<String, Object> financialData = new HashMap<>();
        financialData.put("totalBalance", summary.getTotalBalance());
        financialData.put("monthlyIncome", summary.getMonthlyIncome());
        financialData.put("monthlyExpenses", summary.getMonthlyExpenses());
        financialData.put("monthlySavings", summary.getMonthlySavings());
        financialData.put("spendingByCategory", summary.getSpendingByCategory());

        return aiAgentClient.getFinancialAdvice(user.getId(), financialData);
    }

    public String chatWithAiAgent(User user, String message) {
        AnalyticsDTO.DashboardSummary summary = getDashboardSummary(user);
        
        Map<String, Object> context = new HashMap<>();
        context.put("totalBalance", summary.getTotalBalance());
        context.put("monthlyIncome", summary.getMonthlyIncome());
        context.put("monthlyExpenses", summary.getMonthlyExpenses());
        context.put("spendingByCategory", summary.getSpendingByCategory());

        return aiAgentClient.chat(user.getId(), message, context);
    }

    private Map<String, Object> transactionToMap(Transaction transaction) {
        Map<String, Object> map = new HashMap<>();
        map.put("id", transaction.getId());
        map.put("description", transaction.getDescription());
        map.put("amount", transaction.getAmount());
        map.put("type", transaction.getType().name());
        map.put("category", transaction.getCategory());
        map.put("date", transaction.getTransactionDate().toString());
        return map;
    }
}
