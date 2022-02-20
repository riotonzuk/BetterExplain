# SST-2
wget https://dl.fbaipublicfiles.com/glue/data/SST-2.zip
unzip SST-2.zip
rm SST-2.zip
# SST-5
wget https://nlp.stanford.edu/~socherr/stanfordSentimentTreebank.zip
unzip stanfordSentimentTreebank.zip
rm stanfordSentimentTreebank.zip
# TREC
mkdir TREC
cd TREC
wget https://cogcomp.seas.upenn.edu/Data/QA/QC/train_1000.label
wget https://cogcomp.seas.upenn.edu/Data/QA/QC/train_2000.label 
wget https://cogcomp.seas.upenn.edu/Data/QA/QC/train_3000.label
wget https://cogcomp.seas.upenn.edu/Data/QA/QC/train_4000.label
wget https://cogcomp.seas.upenn.edu/Data/QA/QC/train_5500.label
wget https://cogcomp.seas.upenn.edu/Data/QA/QC/TREC_10.label
cd ../
# SUBJ
mkdir movie-review && cd movie-review
wget http://www.cs.cornell.edu/people/pabo/movie-review-data/rotten_imdb.tar.gz
tar -xzvf rotten_imdb.tar.gz
rm rotten_imdb.tar.gz
cd ../../

