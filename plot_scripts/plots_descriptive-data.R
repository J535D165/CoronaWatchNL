library(tidyverse)
library(cowplot)
library(glue)
library(lubridate)
dir.create("plots")

############################
##### DESCRIPTIVE DATA #####
############################

# Age
read_csv("data/rivm_NL_covid19_age.csv") %>%
  filter(LeeftijdGroep != "Niet vermeld") %>%
  mutate(
    groep = ifelse(LeeftijdGroep %in% c("0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"), "0-59", NA),
    groep = ifelse(LeeftijdGroep %in% c("60-64", "65-69", "70-74"), "60-74", groep),
    groep = ifelse(LeeftijdGroep %in% c("75-79", "80-84", "85-89", "90-94", "95+"), "75+", groep)
  ) %>%
  group_by(Datum, groep, Type) %>%
  summarize(Aantal = sum(Aantal)) %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type, linetype=groep)) +
  geom_line() +
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("COVID-19 patiënten per leeftijd") +
  ggsave("plots/overview_plot_leeftijd.png", width = 5.5, height=4)

# Sex
# COVID-19 patiënten per geslacht
## Absolute waarden
read_csv("data/rivm_NL_covid19_sex.csv") %>%
  filter(Geslacht %in% c("Man", "Vrouw")) %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type, linetype= Geslacht)) +
  geom_line() +
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("COVID-19 patiënten per geslacht") +
  ggsave("plots/overview_plot_geslacht.png", width = 5.5, height=4)

## Percentages
sex <- read_csv("data/rivm_NL_covid19_sex.csv") 
sex <- sex %>% filter(Geslacht != "Niet vermeld")
ratio <- (sex %>% filter(Geslacht == "Man")   %>% select(Aantal) /
          sex %>% filter(Geslacht == "Vrouw") %>% select(Aantal))
sex['Ratio'] <- rep(as.matrix(ratio), each =2)

sex %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Ratio, colour = Type)) +
  geom_line() +
  theme_minimal() +
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("COVID-19 patiënten Man:Vrouw ratio") +
  ggsave("plots/ratio_plot_geslacht.png", width = 5.5, height=4)


# TOENAME COVID-19 patiënten per geslacht 
## Absolute waarden
sex <- sex %>% 
  filter(Geslacht == "Man" & Type == "Totaal") %>%
  mutate(Toename = Aantal - lag(Aantal)) %>%
  bind_rows(sex %>% 
              filter(Geslacht == "Man" & Type == "Ziekenhuisopname") %>%
              mutate(Toename = Aantal - lag(Aantal))) %>%
  bind_rows(sex %>% 
              filter(Geslacht == "Man" & Type == "Overleden") %>%
              mutate(Toename = Aantal - lag(Aantal))) %>%
  bind_rows(sex %>% 
              filter(Geslacht == "Vrouw" & Type == "Totaal") %>%
              mutate(Toename = Aantal - lag(Aantal))) %>%
  bind_rows(sex %>% 
              filter(Geslacht == "Vrouw" & Type == "Ziekenhuisopname") %>%
              mutate(Toename = Aantal - lag(Aantal))) %>%
  bind_rows(sex %>% 
              filter(Geslacht == "Vrouw" & Type == "Overleden") %>%
              mutate(Toename = Aantal - lag(Aantal)))

sex %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Toename, colour = Type, linetype= Geslacht)) +
  geom_line() +
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Toename COVID-19 patiënten per geslacht") +
  ggsave("plots/toename_plot_geslacht.png", width = 5.5, height=4)


## Percentages
sex <- sex[order(sex$Datum, sex$Type),]
ratio_toe <- (sex %>% filter(Geslacht == "Man")   %>% select(Toename) /
                sex %>% filter(Geslacht == "Vrouw") %>% select(Toename))
sex['Ratio_toe'] <- rep(as.matrix(ratio_toe), each =2)

sex %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Ratio_toe, colour = Type)) +
  geom_line() +
  theme_minimal() +
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Toename COVID-19 patiënten Man:Vrouw ratio") +
  ggsave("plots/ratio_toename_geslacht.png", width = 5.5, height=4)
