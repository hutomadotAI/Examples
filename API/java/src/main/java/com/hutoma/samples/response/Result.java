package com.hutoma.samples.response;

public class Result {

    private String chatId;
    private ChatResult result;
    private Status status;

    public String getChatId() {
        return this.chatId;
    }

    public ChatResult getResult() {
        return this.result;
    }

    public Status getStatus() {
        return this.status;
    }
}
