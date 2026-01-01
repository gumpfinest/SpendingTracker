package com.smartspend.service;

import com.smartspend.dto.TransactionDTO;
import com.smartspend.entity.Transaction;
import com.smartspend.entity.User;
import com.smartspend.repository.BudgetRepository;
import com.smartspend.repository.TransactionRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class TransactionService {

    private final TransactionRepository transactionRepository;
    private final BudgetRepository budgetRepository;
    private final DataServiceClient dataServiceClient;

    @Transactional
    public TransactionDTO.Response createTransaction(User user, TransactionDTO.CreateRequest request) {
        Transaction transaction = Transaction.builder()
                .user(user)
                .description(request.getDescription())
                .amount(request.getAmount())
                .type(request.getType())
                .status(Transaction.TransactionStatus.PENDING)
                .transactionDate(request.getTransactionDate() != null 
                        ? request.getTransactionDate() 
                        : LocalDateTime.now())
                .notes(request.getNotes())
                .build();

        transaction = transactionRepository.save(transaction);

        // Call data service to categorize the transaction
        String category = dataServiceClient.categorizeTransaction(request.getDescription());
        transaction.setCategory(category);
        transaction.setStatus(Transaction.TransactionStatus.CATEGORIZED);
        transaction = transactionRepository.save(transaction);

        // Update budget if it's an expense
        if (transaction.getType() == Transaction.TransactionType.EXPENSE && category != null) {
            updateBudgetSpending(user, category, request.getAmount());
        }

        return TransactionDTO.Response.fromEntity(transaction);
    }

    public List<TransactionDTO.Response> getUserTransactions(User user) {
        return transactionRepository.findByUserOrderByTransactionDateDesc(user)
                .stream()
                .map(TransactionDTO.Response::fromEntity)
                .collect(Collectors.toList());
    }

    public List<TransactionDTO.Response> getTransactionsByDateRange(
            User user, LocalDateTime startDate, LocalDateTime endDate) {
        return transactionRepository
                .findByUserAndTransactionDateBetweenOrderByTransactionDateDesc(user, startDate, endDate)
                .stream()
                .map(TransactionDTO.Response::fromEntity)
                .collect(Collectors.toList());
    }

    public TransactionDTO.Response getTransaction(User user, Long transactionId) {
        Transaction transaction = transactionRepository.findById(transactionId)
                .orElseThrow(() -> new RuntimeException("Transaction not found"));

        if (!transaction.getUser().getId().equals(user.getId())) {
            throw new RuntimeException("Access denied");
        }

        return TransactionDTO.Response.fromEntity(transaction);
    }

    @Transactional
    public TransactionDTO.Response updateTransaction(
            User user, Long transactionId, TransactionDTO.UpdateRequest request) {
        Transaction transaction = transactionRepository.findById(transactionId)
                .orElseThrow(() -> new RuntimeException("Transaction not found"));

        if (!transaction.getUser().getId().equals(user.getId())) {
            throw new RuntimeException("Access denied");
        }

        if (request.getDescription() != null) {
            transaction.setDescription(request.getDescription());
        }
        if (request.getAmount() != null) {
            transaction.setAmount(request.getAmount());
        }
        if (request.getType() != null) {
            transaction.setType(request.getType());
        }
        if (request.getCategory() != null) {
            transaction.setCategory(request.getCategory());
        }
        if (request.getTransactionDate() != null) {
            transaction.setTransactionDate(request.getTransactionDate());
        }
        if (request.getNotes() != null) {
            transaction.setNotes(request.getNotes());
        }

        transaction.setUpdatedAt(LocalDateTime.now());
        transaction = transactionRepository.save(transaction);

        return TransactionDTO.Response.fromEntity(transaction);
    }

    @Transactional
    public void deleteTransaction(User user, Long transactionId) {
        Transaction transaction = transactionRepository.findById(transactionId)
                .orElseThrow(() -> new RuntimeException("Transaction not found"));

        if (!transaction.getUser().getId().equals(user.getId())) {
            throw new RuntimeException("Access denied");
        }

        transactionRepository.delete(transaction);
    }

    private void updateBudgetSpending(User user, String category, BigDecimal amount) {
        LocalDateTime now = LocalDateTime.now();
        budgetRepository.findByUserAndCategoryAndMonthAndYear(
                user, category, now.getMonthValue(), now.getYear()
        ).ifPresent(budget -> {
            budget.setCurrentSpent(budget.getCurrentSpent().add(amount));
            budget.setUpdatedAt(LocalDateTime.now());
            budgetRepository.save(budget);
        });
    }
}
