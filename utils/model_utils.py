import torch
import os
from collections import OrderedDict


def freeze(model):
    for p in model.parameters():
        p.requires_grad = False


def unfreeze(model):
    for p in model.parameters():
        p.requires_grad = True


def is_frozen(model):
    x = [p.requires_grad for p in model.parameters()]
    return not all(x)


def save_checkpoint(model_dir, state, session):
    epoch = state['epoch']
    model_out_path = os.path.join(model_dir, "model_epoch_{}_{}.pth".format(epoch, session))
    torch.save(state, model_out_path)


def load_checkpoint(model, weights, device):
    checkpoint = torch.load(weights, map_location=device, weights_only=True)
    try:
        model.load_state_dict(checkpoint["state_dict"], strict=False)
    except:
        state_dict = checkpoint["state_dict"]
        new_state_dict = OrderedDict()
        for k, v in state_dict.items():
            name = k[10:]  # remove `module.`
            new_state_dict[name] = v
        model.load_state_dict(new_state_dict, strict=False)
    print("Model loading successfully!")


def load_checkpoint_multigpu(model, weights):
    checkpoint = torch.load(weights)
    state_dict = checkpoint["state_dict"]
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = k[7:]  # remove `module.`
        new_state_dict[name] = v
    model.load_state_dict(new_state_dict)


def load_start_epoch(weights):
    checkpoint = torch.load(weights)
    epoch = checkpoint["epoch"]
    return epoch

def load_best_metrics(weights):
    checkpoint = torch.load(weights)
    return checkpoint["PSNR"], checkpoint["SSIM"]

def load_optim(optimizer, weights):
    checkpoint = torch.load(weights)
    try:
        optimizer.load_state_dict(checkpoint['optimizer'])
    except:
        pass

def network_parameters(nets):
    num_params = sum(param.numel() for param in nets.parameters())
    return num_params
