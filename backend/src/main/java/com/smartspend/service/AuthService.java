package com.smartspend.service;

import com.smartspend.dto.AuthDTO;
import com.smartspend.entity.User;
import com.smartspend.repository.UserRepository;
import com.smartspend.security.JwtService;
import com.smartspend.security.LoginAttemptService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;
    private final LoginAttemptService loginAttemptService;

    public AuthDTO.AuthResponse register(AuthDTO.RegisterRequest request) {
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new RuntimeException("Username already exists");
        }

        User user = User.builder()
                .name(request.getName())
                .username(request.getUsername())
                .password(passwordEncoder.encode(request.getPassword()))
                .build();

        userRepository.save(user);

        String token = jwtService.generateToken(user);
        return AuthDTO.AuthResponse.of(token, user);
    }

    public AuthDTO.AuthResponse login(AuthDTO.LoginRequest request) {
        String username = request.getUsername();
        
        // Check if account is locked
        if (loginAttemptService.isBlocked(username)) {
            throw new RuntimeException("Account is locked due to too many failed attempts. Try again in 15 minutes.");
        }

        try {
            authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(
                            username,
                            request.getPassword()
                    )
            );

            User user = userRepository.findByUsername(username)
                    .orElseThrow(() -> new RuntimeException("User not found"));

            // Login successful, clear any failed attempts
            loginAttemptService.loginSucceeded(username);

            String token = jwtService.generateToken(user);
            return AuthDTO.AuthResponse.of(token, user);
        } catch (BadCredentialsException e) {
            // Record failed attempt
            loginAttemptService.loginFailed(username);
            int remaining = loginAttemptService.getRemainingAttempts(username);
            if (remaining > 0) {
                throw new RuntimeException("Invalid credentials. " + remaining + " attempts remaining.");
            } else {
                throw new RuntimeException("Account is now locked due to too many failed attempts. Try again in 15 minutes.");
            }
        }
    }
}
