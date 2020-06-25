library(tidyverse)
library(cowplot)
library(glue)
library(lubridate)
dir.create("plots")

###################
##### IC DATA #####
###################


# NICE DATA #
data_nice <- read_csv("data/nice_ic_by_day.csv")

# sort data
data_nice <- data_nice %>%
  select(Datum, newIntake) %>%
  rename("Aantal" = newIntake) %>%
  mutate(meas = "Nieuw per dag") %>%
  bind_rows(data_nice %>%
              select(Datum, intakeCount) %>%
              rename("Aantal" = intakeCount) %>%
              mutate(meas = "Totaal per dag")) %>%
  bind_rows(data_nice %>%
              select(Datum, intakeCumulative) %>%
              rename("Aantal" = intakeCumulative) %>%
              mutate(meas = "Cumulatief")) %>%
  bind_rows(data_nice %>%
              select(Datum, survivedCumulative) %>%
              rename("Aantal" = survivedCumulative) %>%
              mutate(meas = "Overleefd")) %>%
  bind_rows(data_nice %>%
              select(Datum, diedCumulative) %>%
              rename("Aantal" = diedCumulative) %>%
              mutate(meas = "Overleden")) %>%
  bind_rows(data_nice %>%
              select(Datum, icCount) %>%
              rename("Aantal" = icCount) %>%
              mutate(meas = "icCount"))

# plot "IC opnamen"
data_nice %>%
  filter(meas == "Nieuw per dag" |
           meas == "Totaal per dag" |
           meas == "Cumulatief") %>%
  mutate(meas = factor(meas, c("Nieuw per dag", "Totaal per dag", "Cumulatief"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = meas, group = meas)) +
  geom_line()+
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("NICE: Aantal IC-opnamen van COVID-19 patiënten") +
  ggsave("plots/ic_nice_intakes.png", width = 5.5, height=4)

# plot "Vrijkomst IC-bedden"
data_nice %>%
  filter(meas == "Overleefd" |
           meas == "Overleden") %>%
  ggplot(aes(x = Datum, y = Aantal, colour = meas, group = meas)) +
  geom_line()+
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("NICE: Vrijkomst IC-bedden COVID-19 patiënten") +
  ggsave("plots/ic_nice_vrijkomst.png", width = 5.5, height=4)


# LCPS data #
data_lcps <- read_csv("data/lcps_ic.csv")
lcps_country <- read_csv("data/lcps_ic_country.csv")

# plot aantal opnamen
data_lcps %>%
  ggplot(aes(x = Date, y = Aantal)) +
  geom_line(colour = "#E69F00")+
  theme_minimal() +
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  ggtitle("LCPS: Aantal IC-opnamen COVID-19 patiënten") +
  ggsave("plots/ic_lcps_intakes.png", width = 5.5, height=4)

# plot aantal opnamen per land
lcps_country %>%
  mutate(Land = factor(Land, c("Nederland", "Duitsland"))) %>%
  ggplot(aes(x = Datum, y = Aantal, group = Land, linetype = Land)) +
  geom_line(colour = "#E69F00")+
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  ggtitle("LCPS: Aantal IC-opnamen COVID-19 patiënten per land") +
  ggsave("plots/ic_lcps_intakes_country.png", width = 5.5, height=4)

# # NICE & LCSP #
# # Merge nice en lcps data
# data_ic <- data_lcps %>%
#   rename("Datum" = Date) %>%
#   mutate(meas = "Totaal per dag",
#          bron = "LCPS") %>%
#   bind_rows(data_nice %>%
#               mutate(bron = "NICE"))

# # plot combinatie
# data_ic %>%
#   filter(meas == "Totaal per dag") %>%
#   mutate(bron = factor(bron, c("LCPS", "NICE"))) %>%
#   ggplot(aes(x = Datum, y = Aantal, colour = bron)) +
#   geom_line() +
#   scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
#   theme_minimal() +
#   theme(axis.title.x=element_blank(),
#         axis.title.y=element_blank(),
#         legend.pos = "bottom",
#         legend.title = element_blank()) +
#   scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
#   ggtitle("LCPS vs NICE: Totaal aantal IC-opnamen per dag") +
#   ggsave("plots/ic_lcps_nice.png", width = 5.5, height=4)

# # plot combinatie per land
# data_ic_2 <- data_nice %>%
#   mutate(bron = "NICE",
#          Land = "Nederland") %>%
#   bind_rows(lcps_country %>%
#               mutate(bron = "LCPS",
#                      meas = "Totaal per dag") %>%
#               select(Datum, Aantal, meas, bron, Land))
# 
# data_ic_2 %>%
#   filter(meas == "Totaal per dag") %>%
#   mutate(bron = factor(bron, c("LCPS", "NICE")),
#          Land = factor(Land, c("Nederland", "Duitsland"))) %>%
#   ggplot(aes(x = Datum, y = Aantal, group = interaction(Land, bron), colour = bron, linetype = Land)) +
#   geom_line() +
#   scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
#   theme_minimal() +
#   theme(axis.title.x = element_blank(),
#         axis.title.y = element_blank(),
#         legend.pos = "bottom",
#         legend.title = element_blank()) +
#   scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
#   ggtitle("LCPS vs NICE: Aantal IC-opnamen COVID-19 patiënten per land") +
#   ggsave("plots/ic_lcps_nice_country.png", width = 5.5, height=4)



# Laad datasets
RIVM <- read_csv("data-geo/data-national/RIVM_NL_national.csv")
NICE <- read_csv("data/nice_ic_by_day.csv")
LCPS <- read_csv("data/lcps_ic.csv")

# Merge datasets
RIVM <- RIVM %>% filter(Type == "Ziekenhuisopname") %>% select(-AantalCumulatief) %>%
  mutate(Type = "Nieuw per dag",
         Bron = "RIVM",
         Descr = "Ziekenhuisopnamen (RIVM)") %>%
  bind_rows(RIVM %>% filter(Type == "Ziekenhuisopname") %>% select(-Aantal) %>%
              rename("Aantal" = AantalCumulatief) %>%
              mutate(Type = "Totaal",
                     Bron = "RIVM",
                     Descr = "Ziekenhuisopnamen (RIVM)"))
NICE <- NICE %>% select(Datum, newIntake) %>%
  rename("Aantal" = newIntake) %>% mutate(Type = "Nieuw per dag",
                                          Bron = "NICE",
                                          Descr = "IC-opnamen (NICE)") %>%
  bind_rows(NICE %>% select(Datum, intakeCount) %>%
              rename("Aantal" = intakeCount) %>% mutate(Type = "Totaal per dag",
                                                        Bron = "NICE",
                                                        Descr = "IC-opnamen (NICE)")) %>%
  bind_rows(NICE %>% select(Datum, intakeCumulative) %>%
              rename("Aantal" = intakeCumulative) %>% mutate(Type = "Totaal",
                                                             Bron = "NICE",
                                                             Descr = "IC-opnamen (NICE)"))
LCPS <- LCPS %>% mutate(Type = "Totaal per dag",
                        Bron = "LCPS",
                        Descr = "IC-opnamen (incl. schatting) (LCPS)") %>%
  rename("Datum" = Date)
IC <- bind_rows(LCPS, RIVM, NICE)

# # Alle IC-bronnen in één plot geplot
# IC %>%
#   mutate(Type = factor(Type, c("Nieuw per dag", "Totaal per dag", "Totaal")),
#          Bron = factor(Bron, c("NICE", "RIVM", "LCPS"))) %>%
#   ggplot(aes(x = Datum, y = Aantal, colour = Type, linetype = Bron, group = interaction(Bron, Type))) +
#   geom_line() +
#   scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
#   theme_minimal() +
#   theme(axis.title.x=element_blank(),
#         axis.title.y=element_blank(),
#         legend.pos = "bottom",
#         legend.title = element_blank()) +
#   scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
#   ggtitle("Aantal ziekenhuisopnamen volgens RIVM, NICE en LCPS") +
#   ggsave("plots/overview_IC_data.png", width = 5.5, height=4)

# Alle 'Nieuwe' opnamen
kleur <- c("#E69F00", "#56B4E9")
IC %>%
  mutate(Descr = factor(Descr, c("IC-opnamen (NICE)", "Ziekenhuisopnamen (RIVM)", "IC-opnamen (incl. schatting) (LCPS)"))) %>%
  filter(Type == "Nieuw per dag") %>%
  ggplot(aes(x = Datum, y = Aantal, fill = Descr, colour = Descr, group = Descr)) +
  geom_line()+
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  scale_color_manual(values=kleur)+
  scale_fill_manual(values=kleur)+
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  ggtitle("RIVM vs. NICE: Nieuwe ziekenhuis en IC-opnamen per dag") +
  ggsave("plots/overview_IC_nieuw.png", width = 5.5, height=4)

# Alle 'Totaal' opnamen
IC %>%
  mutate(Descr = factor(Descr, c("IC-opnamen (NICE)", "Ziekenhuisopnamen (RIVM)", "IC-opnamen (incl. schatting) (LCPS)"))) %>%
  filter(Type == "Totaal per dag") %>%
  ggplot(aes(x = Datum, y = Aantal, fill = Descr, colour = Descr, group = Descr)) +
  geom_line()+
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  scale_color_manual(values=kleur)+
  scale_fill_manual(values=kleur)+
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  ggtitle("NICE vs. LCPS: Totaal aantal IC-opnamen per dag") +
  ggsave("plots/overview_IC_actueel.png", width = 5.5, height=4)

# Alle 'Cumulatieve' opnamen
IC %>%
  mutate(Descr = factor(Descr, c("IC-opnamen (NICE)", "Ziekenhuisopnamen (RIVM)", "IC-opnamen (incl. schatting) (LCPS)"))) %>%
  filter(Type == "Totaal") %>%
  ggplot(aes(x = Datum, y = Aantal, fill = Descr, colour = Descr, group = Descr)) +
  geom_line()+
  scale_y_continuous(expand = c(0, 0), limits = c(0, NA))+
  scale_color_manual(values=kleur)+
  scale_fill_manual(values=kleur)+
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  ggtitle("RIVM vs. NICE: Cumulatief aantal ziekenhuis en IC-opnamen") +
  ggsave("plots/overview_IC_totaal.png", width = 5.5, height=4)
