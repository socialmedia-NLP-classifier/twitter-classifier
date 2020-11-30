
library(text2vec)
library(data.table)

movie_review = read.csv("cleaned_agg_data.csv")
id_list = seq.int(nrow(movie_review))
for (i in 1:length(id_list)){
  id_list[i] = toString(id_list[i])
}
movie_review$id = id_list
setDT(movie_review)
#summary(movie_review)
#movie_review$id
setkey(movie_review, id)
set.seed(2017L)
all_ids = movie_review$id
train_ids = sample(all_ids, length(all_ids)*0.8)
test_ids = setdiff(all_ids, train_ids)
train = movie_review[J(train_ids)]
test = movie_review[J(test_ids)]
prep_fun = tolower
tok_fun = word_tokenizer

it_train = itoken(train[,clean_comment], 
                  preprocessor = prep_fun, 
                  tokenizer = tok_fun, 
                  ids = train[,id], 
                  progressbar = FALSE)

stop_words = c("i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours")
vocab = create_vocabulary(it_train, ngram=c(1L, 2L)) #, stopwords=stop_words)

#pruned_vocab = prune_vocabulary(vocab, 
#                                term_count_min = 5, 
#                                doc_proportion_max = 0.5,
#                                doc_proportion_min = 0.0001)




vectorizer = vocab_vectorizer(vocab)
#vectorizer = vocab_vectorizer(pruned_vocab)

dtm_train = create_dtm(it_train, vectorizer)

# define tfidf model
tfidf = TfIdf$new()
# fit model to train data and transform train data with fitted model
dtm_train_tfidf = fit_transform(dtm_train, tfidf)
# tfidf modified by fit_transform() call!
# apply pre-trained tf-idf transformation to test data

#dim(dtm_train)
#identical(rownames(dtm_train), train$id)
library(glmnet)
NFOLDS = 4
t1 = Sys.time()
glmnet_classifier = cv.glmnet(x = dtm_train_tfidf, y = train[['category']], 
                              family = 'binomial', 
                              # L1 penalty
                              alpha = 1,
                              # interested in the area under ROC curve
                              type.measure = "auc",
                              # 5-fold cross-validation
                              nfolds = NFOLDS,
                              # high value is less accurate, but has faster training
                              thresh = 1e-3,
                              # again lower number of iterations for faster training
                              maxit = 1e3)
print(difftime(Sys.time(), t1, units = 'sec'))

plot(glmnet_classifier)
print(paste("max AUC =", round(max(glmnet_classifier$cvm), 4)))


# Note that most text2vec functions are pipe friendly!
it_test = tok_fun(prep_fun(test$clean_comment))
# turn off progressbar because it won't look nice in rmd
it_test = itoken(it_test, ids = test$id, progressbar = FALSE)

dtm_test_tfidf = create_dtm(it_test, vectorizer)
dtm_test_tfidf = transform(dtm_test_tfidf, tfidf)


dtm_test = create_dtm(it_test, vectorizer)

preds = predict(glmnet_classifier, dtm_test_tfidf, type = 'response')[,1]
# get the auc score
glmnet:::auc(test$category, preds)

input_vec = c(
  "hello, my name is kukai and I like KFC",
  "fuck you, get off the game",
  "Game of thrones was a great show",
  "I love your youtube contents",
  "I like playing tennis, soccer, football, and running",
  "cave man brain go brrr",
  "I need coffee",
  "my computer has 8gb memory and its really fast",
  "aaaaaaaaaaaaaaaaaa",
  "bob went to a political raly",
  "my book recommendation is catcher in the rye and the great gatsby",
  "jesus f'n crist",
  "gvw, wd gfh g fvwefw fewfwef cwefewf ",
  "art class on Tuesday and the professor is great"
  
)
it_test1 = tok_fun(prep_fun(input_vec))
it_test1 = itoken(it_test1)
dtm_test1 = create_dtm(it_test1, vectorizer)

dtm_test_tfidf1 = create_dtm(it_test1, vectorizer)
dtm_test_tfidf1 = transform(dtm_test_tfidf1, tfidf)


preds = predict(glmnet_classifier, dtm_test_tfidf1, type = 'response')[,1]
preds

for (j in 1:length(input_vec)){
  print(input_vec[j])
  print(preds[j])
}

