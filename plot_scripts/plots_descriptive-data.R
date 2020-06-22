library(tidyverse)
library(cowplot)
library(glue)
library(lubridate)
dir.create("plots")

############################
##### DESCRIPTIVE DATA #####
############################

# AGE
# Toename
read_csv("data-desc/data-age/RIVM_NL_age.csv") %>%
  filter(Datum > "2020-03-23") %>%
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
        legend.text = element_text(size = 8),
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Toename COVID-19 patiënten per leeftijdsgroep") +
  ggsave("plots/overview_plot_leeftijd.png", width = 5.5, height=4)

# Age: Cumulatief
read_csv("data-desc/data-age/RIVM_NL_age.csv") %>%
  filter(LeeftijdGroep != "Niet vermeld") %>%
  mutate(
    groep = ifelse(LeeftijdGroep %in% c("0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"), "0-59", NA),
    groep = ifelse(LeeftijdGroep %in% c("60-64", "65-69", "70-74"), "60-74", groep),
    groep = ifelse(LeeftijdGroep %in% c("75-79", "80-84", "85-89", "90-94", "95+"), "75+", groep)
  ) %>%
  group_by(Datum, groep, Type) %>%
  summarize(Aantal = sum(AantalCumulatief)) %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type, linetype=groep)) +
  geom_line() +
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.text = element_text(size = 8),
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("COVID-19 patiënten per leeftijdsgroep") +
  ggsave("plots/overview_plot_leeftijd_cum.png", width = 5.5, height=4)


# SEX
# Toename
read_csv("data-desc/data-sex/RIVM_NL_sex.csv") %>%
  filter(Datum > "2020-03-23") %>%
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
  ggtitle("Toename COVID-19 patiënten per geslacht") +
  ggsave("plots/toename_plot_geslacht.png", width = 5.5, height=4)

# Sex: Cumulatief
read_csv("data-desc/data-sex/RIVM_NL_sex.csv") %>%
  filter(Geslacht %in% c("Man", "Vrouw")) %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = AantalCumulatief, colour = Type, linetype= Geslacht)) +
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


# Man:Vrouw ratios 
# Toename
sex <- read_csv("data-desc/data-sex/RIVM_NL_sex.csv")
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
  ggtitle("Toename COVID-19 patiënten Man:Vrouw ratio") +
  ggsave("plots/ratio_toename_geslacht.png", width = 5.5, height=4)

# Cumulatief
sex <- read_csv("data-desc/data-sex/RIVM_NL_sex.csv")
sex <- sex %>% filter(Geslacht != "Niet vermeld")
ratio <- (sex %>% filter(Geslacht == "Man")   %>% select(AantalCumulatief) /
            sex %>% filter(Geslacht == "Vrouw") %>% select(AantalCumulatief))
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


# AGE & SEX
### Descriptives deceased cases
read_csv("data-desc/data-deceased/RIVM_NL_deceased_age_sex.csv") %>%
  filter(LeeftijdGroep != "Niet vermeld") %>%
  mutate(
    groep = ifelse(LeeftijdGroep %in% c("0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"), "0-59", NA),
    groep = ifelse(LeeftijdGroep %in% c("60-64", "65-69", "70-74"), "60-74", groep),
    groep = ifelse(LeeftijdGroep %in% c("75-79", "80-84", "85-89", "90-94", "95+"), "75+", groep)
  ) %>%
  group_by(Datum, groep, Geslacht) %>%
  summarize(Aantal = sum(AantalCumulatief)) %>%
  ggplot(aes(x = Datum, y = Aantal, group = interaction(Geslacht, groep), colour = Geslacht, linetype=groep)) +
  geom_line() +
  theme_minimal() +
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Totaal overleden gevallen per geslacht en leeftijdsgroep") +
  ggsave("plots/deceased_age_sex.png", width = 5.5, height=4)


read_csv("data-desc/data-deceased/RIVM_NL_deceased_age_sex.csv") %>%
  filter(Datum != "2020-04-07") %>%
  filter(LeeftijdGroep != "Niet vermeld") %>%
  mutate(
    groep = ifelse(LeeftijdGroep %in% c("0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"), "0-59", NA),
    groep = ifelse(LeeftijdGroep %in% c("60-64", "65-69", "70-74"), "60-74", groep),
    groep = ifelse(LeeftijdGroep %in% c("75-79", "80-84", "85-89", "90-94", "95+"), "75+", groep)
  ) %>%
  group_by(Datum, groep, Geslacht) %>%
  summarize(Aantal = sum(Aantal)) %>%
  ggplot(aes(x = Datum, y = Aantal, group = interaction(Geslacht, groep), colour = Geslacht, linetype=groep)) +
  geom_line() +
  theme_minimal() +
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Overleden gevallen per geslacht en leeftijdsgroep per dag") +
  ggsave("plots/deceased_age_sex_toename.png", width = 5.5, height=4)
