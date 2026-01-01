package com.smartspend.controller;

import com.smartspend.entity.User;
import com.smartspend.service.UserService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/user")
@RequiredArgsConstructor
@Tag(name = "User", description = "User account management endpoints")
public class UserController {

    private final UserService userService;

    @GetMapping("/profile")
    @Operation(summary = "Get current user profile")
    public ResponseEntity<Map<String, Object>> getProfile(@AuthenticationPrincipal User user) {
        return ResponseEntity.ok(Map.of(
            "id", user.getId(),
            "username", user.getUsername(),
            "name", user.getName(),
            "createdAt", user.getCreatedAt().toString(),
            "updatedAt", user.getUpdatedAt().toString()
        ));
    }

    @PutMapping("/profile")
    @Operation(summary = "Update user profile")
    public ResponseEntity<Map<String, Object>> updateProfile(
            @AuthenticationPrincipal User user,
            @RequestBody Map<String, String> request) {
        String name = request.get("name");
        String username = request.get("username");
        
        User updatedUser = userService.updateProfile(user, name, username);
        
        return ResponseEntity.ok(Map.of(
            "message", "Profile updated successfully",
            "user", Map.of(
                "id", updatedUser.getId(),
                "username", updatedUser.getUsername(),
                "name", updatedUser.getName()
            )
        ));
    }

    @PostMapping("/change-password")
    @Operation(summary = "Change user password")
    public ResponseEntity<Map<String, String>> changePassword(
            @AuthenticationPrincipal User user,
            @RequestBody Map<String, String> request) {
        String currentPassword = request.get("currentPassword");
        String newPassword = request.get("newPassword");
        
        userService.changePassword(user, currentPassword, newPassword);
        
        return ResponseEntity.ok(Map.of("message", "Password changed successfully"));
    }

    @DeleteMapping("/account")
    @Operation(summary = "Delete user account")
    public ResponseEntity<Map<String, String>> deleteAccount(
            @AuthenticationPrincipal User user,
            @RequestBody Map<String, String> request) {
        String password = request.get("password");
        
        userService.deleteAccount(user, password);
        
        return ResponseEntity.ok(Map.of("message", "Account deleted successfully"));
    }

    @GetMapping("/stats")
    @Operation(summary = "Get account statistics")
    public ResponseEntity<Map<String, Object>> getAccountStats(@AuthenticationPrincipal User user) {
        return ResponseEntity.ok(userService.getAccountStats(user));
    }

    @GetMapping("/export")
    @Operation(summary = "Export all user data (GDPR compliance)")
    public ResponseEntity<Map<String, Object>> exportData(@AuthenticationPrincipal User user) {
        return ResponseEntity.ok(userService.exportUserData(user));
    }
}
