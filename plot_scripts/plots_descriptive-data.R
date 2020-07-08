library(tidyverse)
library(cowplot)
library(glue)
library(lubridate)
library(pracma)
dir.create("plots")

############################
##### DESCRIPTIVE DATA #####
############################

##########
# AGE
# Toename
# read_csv("data-desc/data-age/RIVM_NL_age.csv") %>%
#   filter(Datum > "2020-03-23") %>%
#   filter(LeeftijdGroep != "Niet vermeld") %>%
#   mutate(
#     groep = ifelse(LeeftijdGroep %in% c("0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"), "0-59", NA),
#     groep = ifelse(LeeftijdGroep %in% c("60-64", "65-69", "70-74"), "60-74", groep),
#     groep = ifelse(LeeftijdGroep %in% c("75-79", "80-84", "85-89", "90-94", "95+"), "75+", groep)
#   ) %>%
#   group_by(Datum, groep, Type) %>%
#   summarize(Aantal = sum(Aantal)) %>%
#   mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
#   ggplot(aes(x = Datum, y = Aantal, colour = Type, linetype=groep)) +
#   geom_line() +
#   scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
#   theme_minimal() +
#   theme(axis.title.x=element_blank(),
#         axis.title.y=element_blank(),
#         legend.pos = "bottom",
#         legend.text = element_text(size = 8),
#         legend.title = element_blank()) +
#   scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
#   ggtitle("Toename COVID-19 patiënten per leeftijdsgroep") +
#   ggsave("plots/overview_plot_leeftijd.png", width = 5.5, height=4)

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

# Voortschrijdend gemiddelde
# Sex: Toename - Voortschrijdend gemiddelde
age <- read_csv("data-desc/data-age/RIVM_NL_age.csv") 
age <- age %>% group_by(LeeftijdGroep, Type) %>% mutate(Aantal = AantalCumulatief - lag(AantalCumulatief)) %>% ungroup()

age_old <- age %>% filter(LeeftijdGroep != "Niet vermeld" & Datum < as.Date('2020-07-07'))
age_new <- age %>% filter(LeeftijdGroep != "Niet vermeld" & Datum >= as.Date('2020-07-07'))

age_old <- age_old %>% 
  group_by(LeeftijdGroep, Type, Datum) %>% 
  summarise(Aantal = sum(Aantal, na.rm = TRUE)) %>% 
  arrange(Datum) %>% 
  mutate(Aantal_ma = movavg(Aantal, 3, "s")) %>%
  ungroup()

age_new <- age_new %>% 
  group_by(LeeftijdGroep, Type, Datum) %>% 
  summarise(Aantal = sum(Aantal, na.rm = TRUE)) %>% 
  arrange(Datum) %>% 
  mutate(Aantal_ma = Aantal / 7) %>%
  ungroup()

age2 <- age_old %>% bind_rows(age_new)

age2 %>%
  filter(Datum > "2020-03-23") %>%
  filter(LeeftijdGroep != "Niet vermeld") %>%
  mutate(
    groep = ifelse(LeeftijdGroep %in% c("0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"), "0-59", NA),
    groep = ifelse(LeeftijdGroep %in% c("60-64", "65-69", "70-74"), "60-74", groep),
    groep = ifelse(LeeftijdGroep %in% c("75-79", "80-84", "85-89", "90-94", "95+"), "75+", groep)
  ) %>%
  group_by(Datum, groep, Type) %>%
  summarize(Aantal_ma = sum(Aantal_ma)) %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Aantal_ma, colour = Type, linetype=groep)) +
  geom_line() +
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.text = element_text(size = 8),
        legend.title = element_blank(),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5)) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  geom_vline(xintercept=as.Date('2020-07-01'), linetype = 2, color = 'gray') +
  labs(subtitle = 'Gemiddeld over de afgelopen 3 dagen', caption = 'Vanaf 1 juli wordt toename per dag bepaald door week-toename gedeeld door 7') +
  ggtitle("Toename COVID-19 patiënten per leeftijdsgroep") +
  ggsave("plots/overview_plot_leeftijd.png", width = 5.5, height=4)

###################
# SEX
# Toename
# read_csv("data-desc/data-sex/RIVM_NL_sex.csv") %>%
#   filter(Datum > "2020-03-23") %>%
#   filter(Geslacht %in% c("Man", "Vrouw")) %>%
#   mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
#   ggplot(aes(x = Datum, y = Aantal, colour = Type, linetype= Geslacht)) +
#   geom_line() +
#   scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
#   theme_minimal() +
#   theme(axis.title.x=element_blank(),
#         axis.title.y=element_blank(),
#         legend.pos = "bottom",
#         legend.title = element_blank()) +
#   scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
#   ggtitle("Toename COVID-19 patiënten per geslacht") +
#   ggsave("plots/toename_plot_geslacht.png", width = 5.5, height=4)

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

# Sex: Toename - Voortschrijdend gemiddelde
sex <- read_csv("data-desc/data-sex/RIVM_NL_sex.csv")
sex <- sex %>% group_by(Geslacht, Type) %>% mutate(Aantal = AantalCumulatief - lag(AantalCumulatief)) %>% ungroup()

sex_old <- sex %>% filter(Geslacht != "Niet vermeld" & Datum < as.Date('2020-07-07'))
sex_new <- sex %>% filter(Geslacht != "Niet vermeld" & Datum >= as.Date('2020-07-07'))

sex_old <- sex_old %>% 
  group_by(Geslacht, Type, Datum) %>% 
  summarise(Aantal = sum(Aantal, na.rm = TRUE)) %>% 
  arrange(Datum) %>% 
  mutate(Aantal_ma = movavg(Aantal, 3, "s")) %>%
  ungroup()

sex_new <- sex_new %>% 
  group_by(Geslacht, Type, Datum) %>% 
  summarise(Aantal = sum(Aantal, na.rm = TRUE)) %>% 
  arrange(Datum) %>% 
  mutate(Aantal_ma = Aantal / 7) %>%
  ungroup()

sex2 <- sex_old %>% bind_rows(sex_new)

sex2 %>%
  filter(Datum > "2020-03-23") %>%
  filter(Geslacht %in% c("Man", "Vrouw")) %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Aantal_ma, colour = Type, linetype= Geslacht)) +
  geom_line() +
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank(),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5)) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  labs(subtitle = 'Gemiddeld over de afgelopen 3 dagen', caption = 'Vanaf 1 juli wordt toename per dag bepaald door week-toename gedeeld door 7') +
  geom_vline(xintercept=as.Date('2020-07-01'), linetype = 2, color = 'gray') +
  ggtitle("Toename COVID-19 patiënten per geslacht") +
  ggsave("plots/toename_plot_geslacht.png", width = 5.5, height=4)

# Man:Vrouw ratios 
# Toename
sex <- read_csv("data-desc/data-sex/RIVM_NL_sex.csv")
sex <- sex %>% group_by(Geslacht, Type) %>% mutate(Aantal = AantalCumulatief - lag(AantalCumulatief)) %>% ungroup()
sex <- sex %>% filter(Geslacht != "Niet vermeld")

man <- movavg((sex %>% filter(Geslacht == "Man")%>% select(Aantal) %>% as.matrix), n = 7, type = 's')
vrouw <- movavg((sex %>% filter(Geslacht == "Vrouw")%>% select(Aantal) %>% as.matrix), n = 7, type = 's')
ratio <- man / vrouw

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
        legend.title = element_blank(),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5)) +
  labs(subtitle = 'Gemiddeld over de afgelopen 7 dagen') +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Toename COVID-19 patiënten Man:Vrouw ratio") +
  ggsave("plots/ratio_toename_geslacht.png", width = 5.5, height=4)

# Cumulatief
sex <- read_csv("data-desc/data-sex/RIVM_NL_sex.csv")
sex <- sex %>% filter(Geslacht != "Niet vermeld")

man <- movavg((sex %>% filter(Geslacht == "Man")%>% select(AantalCumulatief) %>% as.matrix), n = 7, type = 's')
vrouw <- movavg((sex %>% filter(Geslacht == "Vrouw")%>% select(AantalCumulatief) %>% as.matrix), n = 7, type = 's')
ratio <- man / vrouw

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
        legend.title = element_blank(),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5)) +
  labs(subtitle = 'Gemiddeld over de afgelopen 7 dagen') +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("COVID-19 patiënten Man:Vrouw ratio") +
  ggsave("plots/ratio_plot_geslacht.png", width = 5.5, height=4)

###########
# AGE & SEX
### Cumulatief: Descriptives deceased cases
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
  ggtitle("Overleden patiënten per geslacht en leeftijdsgroep") +
  ggsave("plots/deceased_age_sex.png", width = 5.5, height=4)

# Voortschrijdend gemiddelde
sam <- read_csv("data-desc/data-deceased/RIVM_NL_deceased_age_sex.csv") 
sam <- sam %>% group_by(LeeftijdGroep, Geslacht) %>% mutate(Aantal = AantalCumulatief - lag(AantalCumulatief)) %>% ungroup()

sam_old <- sam %>% filter(LeeftijdGroep != "Niet vermeld" & Datum < as.Date('2020-07-07'))
sam_new <- sam %>% filter(LeeftijdGroep != "Niet vermeld" & Datum >= as.Date('2020-07-07'))

sam_old <- sam_old %>% 
  group_by(LeeftijdGroep, Geslacht, Datum) %>% 
  summarise(Aantal = sum(Aantal, na.rm = TRUE)) %>% 
  arrange(Datum) %>% 
  mutate(Aantal_ma = movavg(Aantal, 3, "s")) %>%
  ungroup()

sam_new <- sam_new %>% 
  group_by(Datum, Geslacht, LeeftijdGroep) %>% 
  summarise(Aantal = sum(Aantal, na.rm = TRUE)) %>% 
  arrange(Datum) %>% 
  mutate(Aantal_ma = Aantal / 7) %>%
  ungroup()

samen <- sam_old %>% bind_rows(sam_new)

samen %>%
  filter(Datum != "2020-04-07") %>%
  filter(LeeftijdGroep != "Niet vermeld") %>%
  mutate(
    groep = ifelse(LeeftijdGroep %in% c("0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"), "0-59", NA),
    groep = ifelse(LeeftijdGroep %in% c("60-64", "65-69", "70-74"), "60-74", groep),
    groep = ifelse(LeeftijdGroep %in% c("75-79", "80-84", "85-89", "90-94", "95+"), "75+", groep)
  ) %>%
  group_by(Datum, Geslacht, groep) %>%
  summarize(Aantal = sum(Aantal_ma)) %>%
  ggplot(aes(x = Datum, y = Aantal, group = interaction(Geslacht, groep), colour = Geslacht, linetype=groep)) +
  geom_line() +
  theme_minimal() +
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank(),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5)) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  labs(subtitle = 'Gemiddeld over de afgelopen 3 dagen', caption = 'Vanaf 1 juli wordt toename per dag bepaald door week-toename gedeeld door 7') +
  ggtitle("Overleden patiënten per geslacht en leeftijdsgroep per dag") +
  geom_vline(xintercept=as.Date('2020-07-01'), linetype = 2, color = 'gray') +
  ggsave("plots/deceased_age_sex_toename.png", width = 5.5, height=4)


# Toename
# read_csv("data-desc/data-deceased/RIVM_NL_deceased_age_sex.csv") %>%
#   filter(Datum != "2020-04-07") %>%
#   filter(LeeftijdGroep != "Niet vermeld") %>%
#   mutate(
#     groep = ifelse(LeeftijdGroep %in% c("0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"), "0-59", NA),
#     groep = ifelse(LeeftijdGroep %in% c("60-64", "65-69", "70-74"), "60-74", groep),
#     groep = ifelse(LeeftijdGroep %in% c("75-79", "80-84", "85-89", "90-94", "95+"), "75+", groep)
#   ) %>%
#   group_by(Datum, groep, Geslacht) %>%
#   summarize(Aantal = sum(Aantal)) %>%
#   ggplot(aes(x = Datum, y = Aantal, group = interaction(Geslacht, groep), colour = Geslacht, linetype=groep)) +
#   geom_line() +
#   theme_minimal() +
#   scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
#   theme(axis.title.x=element_blank(),
#         axis.title.y=element_blank(),
#         legend.pos = "bottom",
#         legend.title = element_blank()) +
#   scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
#   ggtitle("Overleden patiënten per geslacht en leeftijdsgroep per dag") +
#   ggsave("plots/deceased_age_sex_toename.png", width = 5.5, height=4)

