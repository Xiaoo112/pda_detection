from torchvision import transforms as tfm
import torch
from torch import nn
import torch.nn.functional as F


class ImageTransforms:
    def __init__(self, res: int):

        self._tfms_train = tfm.Compose([
            tfm.Resize(res),
            tfm.CenterCrop(res),
            tfm.RandomEqualize(p=0.5),
            tfm.RandAugment(),
            tfm.ToTensor(),
            tfm.RandomErasing(scale=(0.02, 0.1)),
            tfm.Normalize(mean=torch.Tensor([0.4850, 0.4560, 0.4060]), std=torch.Tensor([0.2290, 0.2240, 0.2250])),
            tfm.RandomHorizontalFlip(),
            tfm.RandomRotation((-45, 45)),
            tfm.RandomInvert()
        ])

        self._tfms_test = tfm.Compose([
            tfm.Resize(res),
            tfm.CenterCrop(res),
            tfm.ToTensor(),
            tfm.Normalize(mean=torch.Tensor([0.4850, 0.4560, 0.4060]), std=torch.Tensor([0.2290, 0.2240, 0.2250])),
        ])

    def get_transforms(self, key):
        implemented_keys = ['train', 'test']
        if key == 'train':
            return self._tfms_train
        elif key == 'test':
            return self._tfms_test
        else:
            raise NotImplementedError(f"Transform {key} is not implemented. Choose one of {implemented_keys}.")


class VideoTransforms:
    def __init__(self, res: int):

        self._tfms_train = tfm.Compose([
            tfm.RandomEqualize(p=0.5),
            tfm.RandAugment(),
            tfm.ConvertImageDtype(torch.float32),
            tfm.Normalize(0,255),
            nn.UpsamplingBilinear2d(res),
            tfm.CenterCrop(res),
            tfm.RandomErasing(scale=(0.02, 0.1)),
            tfm.Normalize(mean=torch.Tensor([0.4850, 0.4560, 0.4060]), std=torch.Tensor([0.2290, 0.2240, 0.2250])),
            tfm.RandomHorizontalFlip(),
            tfm.RandomRotation((-45, 45)),
            tfm.RandomInvert()
        ])

        self._tfms_test = tfm.Compose([
            tfm.ConvertImageDtype(torch.float32),
            tfm.Normalize(0, 255),
            nn.UpsamplingBilinear2d(res),
            tfm.CenterCrop(res),
            tfm.Normalize(mean=torch.Tensor([0.4850, 0.4560, 0.4060]), std=torch.Tensor([0.2290, 0.2240, 0.2250])),
        ])

    def get_transforms(self, key):
        implemented_keys = ['train', 'test']
        if key == 'train':
            return self._tfms_train
        elif key == 'test':
            return self._tfms_test
        else:
            raise NotImplementedError(f"Transform {key} is not implemented. Choose one of {implemented_keys}.")


class CustomCrop(nn.Module):
    def __init__(self, x0, y0, w, h):
        super().__init__()

        self.x_slice = slice(x0, x0 + w)
        self.y_slice = slice(y0, y0 + h)

    def forward(self, img):
        return img[..., self.y_slice, self.x_slice]