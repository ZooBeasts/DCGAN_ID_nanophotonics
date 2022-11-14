import torch
from torch import nn
import cv2
from Dataloader import MMIDataset
import numpy as np

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# load the saved trained Generator info
model_path = r''


# Load the dataset
dataset = MMIDataset(img_size=64,
                     z_dim=300,
                     points_path=r'',
                     img_folder=r'')

# Output the results path & load the data into Generator
results_folder = r''
gen = torch.load(model_path)
gen = gen.to(device)
gen = gen.eval()

# Generate the image array from given dataset
def predict(net: nn.Module, points):
    return net(points).squeeze(0).squeeze(0).cpu().detach().numpy()

# Generate the desired number of results and save to path
stop_p = 10
i = 0
for p in dataset:
    if i >= stop_p:
        break
    data = p[0].to(device, dtype=torch.float).unsqueeze(0)
    img_out = predict(gen,data)
    img = (img_out + 1) / 2
    img = np.round(255 * img)

    cv2.imwrite(results_folder + '\\' + str(i) + '-test.png', img)
    i += 1

