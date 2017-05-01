library(dplyr)
library(gdata)
#Reading the data
a=read.xls("Tab_Villages.xlsx", sheet = 1, header=TRUE)
b=read.xls("Tab_Villages.xlsx", sheet = 2, header=TRUE)
#Checking NA values
colSums(is.na(a))
colSums(is.na(b))
str(a)
str(b)
#Converting in proper format
a$Survey.Date=as.Date(a$Survey.Date,"%d-%b-%Y")
b$SurveyStartDate=as.Date(b$SurveyStartDate,"%d-%b-%Y")
b$SurveyEndDate=as.Date(b$SurveyEndDate,"%d-%b-%Y")
b$AC.Name=as.character(b$AC.Name)
b$Mandal.Name=as.character(b$Mandal.Name)
b$Village.Name=as.character(b$Village.Name)
#applying join to get required output
output_with_village=inner_join(a[,1:3],b, by=c("Tab.No"))%>%
  mutate(Village.Name = ifelse(Survey.Date>=SurveyStartDate & Survey.Date<=SurveyEndDate, Village.Name ,NA))%>%
  filter(!is.na(Village.Name))%>%
  select(Response.No,Tab.No,Survey.Date,AC.Name,Mandal.Name,Village.Name)
#reading structure and writing it to CSV
str(output_with_village)
write.csv(output_with_village,"Output_with_village_name.csv")

