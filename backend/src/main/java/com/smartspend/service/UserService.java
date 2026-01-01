package com.smartspend.service;

import com.smartspend.entity.User;
import com.smartspend.repository.BudgetRepository;
import com.smartspend.repository.TransactionRepository;
import com.smartspend.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final TransactionRepository transactionRepository;
    private final BudgetRepository budgetRepository;
    private final PasswordEncoder passwordEncoder;

    public User getCurrentUser(User user) {
        return userRepository.findById(user.getId())
                .orElseThrow(() -> new RuntimeException("User not found"));
    }

    @Transactional
    public User updateProfile(User user, String name, String username) {
        User existingUser = userRepository.findById(user.getId())
                .orElseThrow(() -> new RuntimeException("User not found"));

        // Check if new username is already taken by another user
        if (!existingUser.getUsername().equals(username) && 
            userRepository.existsByUsername(username)) {
            throw new RuntimeException("Username already taken");
        }

        existingUser.setName(name);
        existingUser.setUsername(username);
        existingUser.setUpdatedAt(LocalDateTime.now());

        return userRepository.save(existingUser);
    }

    @Transactional
    public void changePassword(User user, String currentPassword, String newPassword) {
        User existingUser = userRepository.findById(user.getId())
                .orElseThrow(() -> new RuntimeException("User not found"));

        // Verify current password
        if (!passwordEncoder.matches(currentPassword, existingUser.getPassword())) {
            throw new RuntimeException("Current password is incorrect");
        }

        existingUser.setPassword(passwordEncoder.encode(newPassword));
        existingUser.setUpdatedAt(LocalDateTime.now());

        userRepository.save(existingUser);
    }

    @Transactional
    public void deleteAccount(User user, String password) {
        User existingUser = userRepository.findById(user.getId())
                .orElseThrow(() -> new RuntimeException("User not found"));

        // Verify password before deletion
        if (!passwordEncoder.matches(password, existingUser.getPassword())) {
            throw new RuntimeException("Password is incorrect");
        }

        // Delete all user's budgets
        budgetRepository.deleteByUserId(user.getId());

        // Delete all user's transactions
        transactionRepository.deleteByUserId(user.getId());

        // Delete the user
        userRepository.delete(existingUser);
    }

    public Map<String, Object> getAccountStats(User user) {
        long transactionCount = transactionRepository.countByUserId(user.getId());
        long budgetCount = budgetRepository.countByUserId(user.getId());
        
        return Map.of(
            "transactionCount", transactionCount,
            "budgetCount", budgetCount,
            "accountCreated", user.getCreatedAt().toString(),
            "lastUpdated", user.getUpdatedAt().toString()
        );
    }

    @Transactional
    public Map<String, Object> exportUserData(User user) {
        var transactions = transactionRepository.findByUserIdOrderByTransactionDateDesc(user.getId());
        var budgets = budgetRepository.findByUserId(user.getId());
        
        return Map.of(
            "user", Map.of(
                "username", user.getUsername(),
                "name", user.getName(),
                "createdAt", user.getCreatedAt().toString()
            ),
            "transactions", transactions,
            "budgets", budgets,
            "exportedAt", LocalDateTime.now().toString()
        );
    }
}
