package com.smartspend.security;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Service to track failed login attempts and implement account lockout.
 * This helps prevent brute-force attacks.
 */
@Service
@RequiredArgsConstructor
public class LoginAttemptService {

    // Max failed attempts before lockout
    private static final int MAX_ATTEMPTS = 5;
    
    // Lockout duration in minutes
    private static final int LOCKOUT_MINUTES = 15;

    // Track attempts: username -> LoginAttemptInfo
    private final Map<String, LoginAttemptInfo> attemptsCache = new ConcurrentHashMap<>();

    public void loginSucceeded(String username) {
        attemptsCache.remove(username);
    }

    public void loginFailed(String username) {
        LoginAttemptInfo info = attemptsCache.getOrDefault(username, new LoginAttemptInfo());
        info.attempts++;
        info.lastAttempt = LocalDateTime.now();
        attemptsCache.put(username, info);
    }

    public boolean isBlocked(String username) {
        LoginAttemptInfo info = attemptsCache.get(username);
        if (info == null) {
            return false;
        }

        // Check if lockout has expired
        if (info.attempts >= MAX_ATTEMPTS) {
            LocalDateTime lockoutEnd = info.lastAttempt.plusMinutes(LOCKOUT_MINUTES);
            if (LocalDateTime.now().isAfter(lockoutEnd)) {
                // Lockout expired, reset
                attemptsCache.remove(username);
                return false;
            }
            return true;
        }
        return false;
    }

    public int getRemainingAttempts(String username) {
        LoginAttemptInfo info = attemptsCache.get(username);
        if (info == null) {
            return MAX_ATTEMPTS;
        }
        return Math.max(0, MAX_ATTEMPTS - info.attempts);
    }

    public LocalDateTime getLockoutEndTime(String username) {
        LoginAttemptInfo info = attemptsCache.get(username);
        if (info == null || info.attempts < MAX_ATTEMPTS) {
            return null;
        }
        return info.lastAttempt.plusMinutes(LOCKOUT_MINUTES);
    }

    private static class LoginAttemptInfo {
        int attempts = 0;
        LocalDateTime lastAttempt = LocalDateTime.now();
    }
}
