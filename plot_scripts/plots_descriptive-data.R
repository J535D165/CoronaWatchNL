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
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("COVID-19 patiënten per leeftijd") +
  ggsave("plots/overview_plot_leeftijd.png", width = 5.5, height=4)

# Sex
read_csv("data/rivm_NL_covid19_sex.csv") %>%
  filter(Geslacht %in% c("Man", "Vrouw")) %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type, linetype= Geslacht)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("COVID-19 patiënten per geslacht") +
  ggsave("plots/overview_plot_geslacht.png", width = 5.5, height=4)

