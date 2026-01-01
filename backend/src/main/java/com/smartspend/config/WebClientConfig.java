package com.smartspend.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class WebClientConfig {

    @Value("${services.data-service.url}")
    private String dataServiceUrl;

    @Value("${services.ai-agent.url}")
    private String aiAgentUrl;

    @Bean(name = "dataServiceWebClient")
    public WebClient dataServiceWebClient() {
        return WebClient.builder()
                .baseUrl(dataServiceUrl)
                .build();
    }

    @Bean(name = "aiAgentWebClient")
    public WebClient aiAgentWebClient() {
        return WebClient.builder()
                .baseUrl(aiAgentUrl)
                .build();
    }
}
