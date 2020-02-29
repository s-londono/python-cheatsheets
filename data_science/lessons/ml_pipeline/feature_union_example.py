# Say you wanted to extract two different kinds of features from the same text column - tfidf values,
# and the length of the text
# If you have a custom transformer called TextLengthExtractor. Now, you could leave X_train as just the original
# text column, if you could figure out how to add the text length extractor to your pipeline. If only you could fit
# it on the original text data, rather than the output of the previous transformer. But you need both the
# outputs of TfidfTransformer and TextLengthExtractor to feed into the classifier as input.
# - Feature unions are super helpful for handling these situations, where we need to run two steps in parallel
# on the same data and combine their results to pass into the next step.
# - Like pipelines, feature unions are built using a list of (key, value) pairs, where the key is the string that
# you want to name a step, and the value is the estimator object. Also like pipelines, feature unions combine a
# list of estimators to become a single estimator. However, a feature union runs its estimators in parallel,
# rather than in a sequence as a pipeline does

X = df['text'].values
y = df['label'].values
X_train, X_test, y_train, y_test = train_test_split(X, y)

pipeline = Pipeline([
    ('features', FeatureUnion([

        ('nlp_pipeline', Pipeline([
            ('vect', CountVectorizer()
            ('tfidf', TfidfTransformer())
        ])),

        ('txt_len', TextLengthExtractor())
    ])),

    ('clf', RandomForestClassifier())
])

# train classifier
pipeline.fit(Xtrain)

# predict on test data
predicted = pipeline.predict(Xtest)


