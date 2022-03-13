import pytorch_lightning
from pytorch_lightning.callbacks import ModelCheckpoint, LearningRateMonitor
import random
import numpy as np
import pytorch_lightning as pl
import logging
from argparse import ArgumentParser
import resource
from data import ClassificationData
from SE_XLNet import SEXLNet

def get_train_steps(dm):
  total_devices = args.num_gpus * args.num_nodes
  train_batches = len(dm.train_dataloader()) // total_devices
  return (args.max_epochs * train_batches) // 1#args.accumulate_grad_batches

rlimit = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (4096, rlimit[1]))

# argparser
parser = ArgumentParser()
parser.add_argument('--num_gpus', type=int)
parser.add_argument('--batch_size', type=int, default=16)
parser.add_argument('--clip_grad', type=float, default=1.0)
parser.add_argument("--dataset_basedir", help="Base directory where the dataset is located.", type=str)
parser.add_argument("--concept_store", help="Concept store file", type=str)
parser.add_argument("--model_name", default='xlnet-base-cased', help="Model to use.")
parser.add_argument("--gamma", default=0.01, type=float, help="Gamma parameter")
parser.add_argument("--lamda", default=0.01, type=float, help="Lamda Parameter")
parser.add_argument("--topk", default=100, type=int,help="Topk GIL concepts")
parser.add_argument("--seed", default=18, type=int,help="Random Seed for reproducibitiliy.")

parser = pl.Trainer.add_argparse_args(parser)
parser = SEXLNet.add_model_specific_args(parser)

args = parser.parse_args()
args.num_gpus = len(str(args.gpus).split(","))

# init: important to make sure every node initializes the same weights
seed = args.seed
np.random.seed(seed)
random.seed(seed)
pl.utilities.seed.seed_everything(seed)
pytorch_lightning.seed_everything(seed)


logging.basicConfig(level=logging.INFO)

# Step 1: Init Data
logging.info("Loading the data module")
dm = ClassificationData(basedir=args.dataset_basedir, tokenizer_name=args.model_name, batch_size=args.batch_size)


# Step 2: Init Model
logging.info("Initializing the model")
model = SEXLNet(hparams=args)
model.hparams.warmup_steps = 0#int(get_train_steps(dm) * model.hparams.warmup_prop)
lr_monitor = LearningRateMonitor(logging_interval='step')

# Step 3: Start
logging.info("Starting the training")
checkpoint_callback = ModelCheckpoint(
    filename='{epoch}-{step}-{val_acc_epoch:.4f}',
    save_top_k=3,
    verbose=True,
    monitor='val_acc_epoch',
    mode='max'
)

try:
  trainer = pl.Trainer.from_argparse_args(args, callbacks=[checkpoint_callback], val_check_interval=0.5, gradient_clip_val=args.clip_grad, track_grad_norm=2)
  trainer.fit(model, dm)
except Exception as e:
  print('training failed!', e)
finally:
  # trainer.test(model, dm)
  # print(checkpoint_callback.best_model_path)
  # model.load_from_checkpoint(checkpoint_callback.best_model_path)
  print("Using {} as best model weights...".format(checkpoint_callback.best_model_path))
  trainer.test(ckpt_path=checkpoint_callback.best_model_path, datamodule=dm)
