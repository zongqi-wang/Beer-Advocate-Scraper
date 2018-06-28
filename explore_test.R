brew = read.csv("breweryinfo.csv", stringsAsFactors = FALSE)
beer = read.csv("beerinfo.csv", stringsAsFactors = FALSE)
#comments = read.csv("comment.csv", stringsAsFactors = FALSE)

dim(brew)
dim(beer)
head(beer)

head(brew)
hist(brew$beers)
sort(table(brew$beers),decreasing = TRUE)
brew[which(brew$beers>450), ]

order(brew$beers, decreasing = TRUE)
brew[7534,]
sort(table(brew[which(brew$country=="Canada"),"province"]),decreasing=TRUE)[1:13]
uni_brew_num <- unique(beer$brewery_number)

sub_brew <- subset(brew, brew$brewery_number %in% uni_brew_num)
dim(sub_brew)
dim(brew)
sub_brew[which(sub_brew$beers>450), c("beer_ratings", "beer_reviews",  "beer_score", "beers","brewery_name")]

plot(log10(table(sub_brew$country)), main="Number of Breweries per country in Log Scale", ylab="Breweries")

rownames(sub_brew) <- seq(length=nrow(sub_brew))

sub_brew[which(sub_brew$country=="Utah"),"country"]="United States"
sub_brew[which(sub_brew$country=="Utah"),]
sub_brew[9006,"country"] = "United States"
sub_brew[9006,"province"] = "Utah"
sub_brew[9006, "city"] = "Utah"
rownames(sub_brew) <- seq(length=nrow(sub_brew))
sub_brew[9006,]

library(ggplot2)
library(rworldmap)
country_t <- table(sub_brew$country)
ggplot(as.data.frame(country_t), aes(x = Var1))+geom_bar()

plot(country_t)

n <- joinCountryData2Map(sub_brew, joinCode = 'NAME', nameJoinColumn = "country")

sub_brew[sub_brew$country=="Trinidad &amp; Tobago","country"] <- "Trinidad and Tobago"
sub_brew[sub_brew$country=="Turks &amp; Caicos Islands","country"] <- "Turks and Caicos Islands"
sub_brew[sub_brew$country=="Sao Tome &amp; Principe", "country"] <- "Sao Tome and Principe"
sub_brew[sub_brew$country=="Bosnia &amp; Herzegovina", "country"] <- "Bosnia and Herzegovina"
sub_brew[sub_brew$country=="Saint Vincent &amp; The Grenadines", "country"] <- "Saint Vincent and The Grenadines"
sub_brew[sub_brew$country=="Antigua &amp; Barbuda", "country"] <- "Antigua and Barbuda"

quantile(as.numeric(sub_brew[,"beers"]))
sub_brew[,"beers"] <- as.numeric(sub_brew[,"beers"])
str(sub_brew[,"beers"])
sub_brew[7611,]

can_brew <- brew[brew$country=="Canada",]
can_beer <- subset(beer, beer$brewery_number %in% can_brew$brewery_number)


sub_brew[] <- lapply(sub_brew, as.character)

ddply(beer, .(style), summarise, Avg_ABV = mean(abv, na.rm=TRUE))


countries.met <- as.data.frame(log10(table(sub_brew$country)))
colnames(countries.met) <- c("country", "value")
n <- joinCountryData2Map(countries.met, joinCode = 'NAME', nameJoinColumn = "country")
mapCountryData(n, nameColumnToPlot = "value", 
               mapTitle="Number of Breweries per Country in log scale", 
               catMethod = "pretty", colourPalette = "diverging")



p_rank <- ddply(total, .(province), summarise, mean_ba = mean(ba_score), mean_abv=mean(abv, na.rm = TRUE))


total <- merge(can_beer[,c("ba_score", "brewery_number", "abv", "beer_name", "beer_number", "brewery_name", "reviews", "style")], can_brew[,c("province", "brewery_number")], by="brewery_number")
p_plot <- ggplot(total, aes(x=abv, y=ba_score, col=province))+geom_jitter()
p_plot <- p_plot+ggtitle("Each Beer in Canada's user score and Alcohol content per Province")+xlab("ABV")+ylab("User Score")
p_plot

s_plot <- ggplot(total, aes(x=province, y=ba_score, col=style))+geom_jitter()
s_plot <- s_plot+ggtitle("Each Beer in Canada's user score and Alcohol content per Province")+xlab("Province")+ylab("User Score")
s_plot + theme(legend.position = "none")



###beer brewery allcomments
###topic allocation for each beer styles
###top 10 words in a topic
###30, 40, 50 topics


###comments

comments = read.csv("fixed_comments.csv", stringsAsFactors = FALSE)
library(RTextTools)
library(topicmodels)
library(tm)
library(SnowballC)
library(dplyr)
dim(comments)
with_comments <- comments[-which(comments$comment==""),]
with_comments <- read.csv("with_comments.csv", stringsAsFactors = FALSE)
with_comments$beer_number <- as.numeric(with_comments$beer_number)

collapsed <- with_comments %>% group_by(beer_number) %>% summarise(comments = paste0(comment, collapse = ". "))
head(collapsed)


(myCorpus = Corpus(VectorSource(collapsed$comments)))

myCorpus <-  tm_map(myCorpus, content_transformer(tolower))
myCorpus <-  tm_map(myCorpus, removeWords, stopwords("english"))
myCorpus <-  tm_map(myCorpus, removePunctuation)
myCorpus <-  tm_map(myCorpus, removeNumbers)
myCorpus <-  tm_map(myCorpus, stripWhitespace)
myCorpusTrim <-  tm_map(myCorpus,stemDocument,language="english")

(dtm = DocumentTermMatrix(myCorpusTrim))
(dtm2 = removeSparseTerms(dtm, 0.98))

rowTotals <- apply(dtm2 , 1, sum) #Find the sum of words in each Document
dtm.new   <- dtm2[rowTotals> 0, ]

remove(collapsed)
remove(myCorpus)
remove(myCorpusTrim)
remove(with_comments)
remove(dtm)
remove(dtm2)

saveRDS(dtm.new, "full_dtm_new.rds")
saveRDS(dtm2, "dtm2.rds")

dtm.new <- readRDS("full_dtm_new.rds")
Gibbs30 = LDA(dtm.new,  30, method = "Gibbs", control = list(burnin = 1000,iter = 5000))
saveRDS(Gibbs30, "gibbs30_full.RDS")
Gibbs40 = LDA(dtm.new,  40, method = "Gibbs", control = list(burnin = 1000,iter = 5000))
saveRDS(Gibbs40, "gibbs40_full.RDS")
Gibbs50 = LDA(dtm.new,  50, method = "Gibbs", control = list(burnin = 1000,iter = 5000))
saveRDS(Gibbs50, "gibbs50_full.RDS")
Gibbs60 = LDA(dtm.new,  60, method = "Gibbs", control = list(burnin = 1000,iter = 5000))
saveRDS(Gibbs60, "gibbs60_full.RDS")




#####Canadian
brew = read.csv("breweryinfo.csv", stringsAsFactors = FALSE)
beer <- read.csv("beerinfo.csv", stringsAsFactors = FALSE)
can_beer <- subset(beer, beer$brewery_number %in% can_brew$brewery_number)
can_brew <- brew[which(brew$country=="Canada"),]
can_com <- subset(with_comments, with_comments$beer_number %in% can_beer$beer_number)


collapsed <- can_com %>% group_by(beer_number) %>% summarise(comments = paste0(comment, collapse = ". "))


(myCorpus = Corpus(VectorSource(collapsed$comments)))

myCorpus <-  tm_map(myCorpus, content_transformer(tolower))
myCorpus <-  tm_map(myCorpus, removeWords, stopwords("english"))
myCorpus <-  tm_map(myCorpus, removePunctuation)
myCorpus <-  tm_map(myCorpus, removeNumbers)
myCorpus <-  tm_map(myCorpus, stripWhitespace)
myCorpus <-  tm_map(myCorpus,stemDocument,language="english")

(dtm <-  DocumentTermMatrix(myCorpus))
(dtm <-  removeSparseTerms(dtm, 0.98))

rowTotals <- apply(dtm , 1, sum) #Find the sum of words in each Document
dtm.new   <- dtm[rowTotals> 0, ]
saveRDS(dtm.new, "can_dtm.RDS")

dtm.new <- readRDS("can_dtm.RDS")

Gibbs30 = LDA(dtm.new,  30, method = "Gibbs", control = list(burnin = 1000,iter = 5000))
saveRDS(Gibbs30, "gibbs30.RDS")
Gibbs40 = LDA(dtm.new,  40, method = "Gibbs", control = list(burnin = 1000,iter = 5000))
saveRDS(Gibbs40, "gibbs40.RDS")
Gibbs50 = LDA(dtm.new,  50, method = "Gibbs", control = list(burnin = 1000,iter = 5000))
saveRDS(Gibbs50, "gibbs50.RDS")
Gibbs60 = LDA(dtm.new,  60, method = "Gibbs", control = list(burnin = 1000,iter = 5000))
saveRDS(Gibbs60, "gibbs60.RDS")
VEM = LDA(can_dtm, k)

Gibbs30 <- readRDS("gibbs50.RDS")
str(Gibbs30)

topics(Gibbs30)
terms(Gibbs30, 10)
