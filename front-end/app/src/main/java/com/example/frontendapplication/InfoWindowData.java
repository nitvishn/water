package com.example.frontendapplication;

public class InfoWindowData {
    private String tanker;
    private String name;
    private String type;
    private String consumption;

    public String getTanker() {
        return tanker;
    }

    public String getName() {
        return name;
    }

    public void setTanker(String tanker) {
        this.tanker = tanker;
    }

    public String getType() {
        return type;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getConsumption() {
        return consumption;
    }

    public void setType(String type) {
        this.type = type;
    }
    public void setConsumption(String consumption) {
        this.consumption = consumption;
    }
}