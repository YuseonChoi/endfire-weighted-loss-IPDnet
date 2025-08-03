from typing import Dict, Optional
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.utilities import rank_zero_only

import os
from torch import Tensor

class MyLogger(TensorBoardLogger):
    # log validation metrics in epochs

    @rank_zero_only
    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None) -> None:
        log = ""
        for k, v in metrics.items():
            _my_step = step
            
            if k.startswith('valid/'):
                epoch = int(metrics['epoch'])
                if not log:
                    log += f"Epoch {epoch} metrics: "
                
                if isinstance(v, Tensor):
                    value = v.item()
                else:
                    value = v
                log += f"{k}={value:.4f}  "
            
            if k.startswith('val/'):  # use epoch for val metrics
                _my_step = int(metrics['epoch'])
            super().log_metrics(metrics={k: v}, step=_my_step)
        
        if log:
            log_file = os.path.join(self.log_dir, "log.txt")
            with open(log_file, "a") as f:
                f.write(log+"\n")
