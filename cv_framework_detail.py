import torch
import torchvision
import torch.utils.data
from torchvision import transforms

# some hyperparameters setting
use_gpu = True
train_batch_size = 64
val_batch_size = 64

if not torch.cuda.is_available():
    use_gpu = False


# First step : prepare your images such as
# train
# ├── a
# │   └── 1.png
# ├── b
# │   └── 2.png
# └── c
#     ├── 3.png
#     └── 4.png

# Second step : Prepare images dataset
# Following is just a demo
custom_transforms_list = [
    # Randomly change the brightness, contrast, saturation and hue of an image
    # hue should be >=0 and <=0.5
    transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.2),
    # interpolation parameters are in PIL.Image
    # Image.NEAREST=0, Image.ANTIALIAS=1, Image.BILINEAR=2, Image.BICUBIC=3
    # size = (height, width)
    transforms.Resize((224, 224), interpolation=3), 
    # torchvision.transforms.Pad(padding, fill=0, padding_mode='constant')
    # fill=(255, 0, 0): red; padding_mode:constant/edge/reflect/symmetric
    # origin [0,1,2]; reflect [2,1,0,1,2,1,0]; symmetric [1,0,0,1,2,2,1]
    transforms.Pad(10, (255, 255, 255), 'constant'),
    transforms.RandomCrop((224, 224)),  
    transforms.RandomHorizontalFlip(),
    # transform Image to Tensor, range to [0, 1], dims from (H, W, C) to (C, H, W)
    transforms.ToTensor(),
    # Normalize parameters from ImageNet
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
]
# Compose the custom transform as a Compose object
custom_transforms = transforms.Compose(custom_transforms_list)

# Load Image Dataset
image_dataset = torchvision.datasets.ImageFolder(
    root="~/data/classified_imgs",
    # A function/transform that takes in an PIL image and returns a transformed version
    transform=custom_transforms, 
    # A function/transform that takes in the label and transforms it
    target_transform=None,
    # A function to load an image given its path
    # loader = PIL.Image.open,
)

# Create an image loader for creating batch data, and speed up load processing
# DataLoader: Combines a dataset and a sampler, and provides single- or multi-process iterators 
# over the dataset
image_loader = torch.utils.data.DataLoader(
    image_dataset,
    batch_size=64,
    # set to True to have the data reshuffled at every epoch, default is false
    shuffle=True,
    # how many subprocesses to use for data loading, 0 means that the data will be loaded
    # in the main process
    num_workers=4,
    # If True, the data loader will copy tensor into cuda pinned memory memory before returning them
    # pinned memory is always in physics memory, and won't swap to virtual memory
    pin_memory=False,
    # if True, drop the last incomplete batch
    drop_last=False,
    # if positive, the timeout value for collecting a batch from workers. Always be non-negtive
    timeout=0)
# Validation dataset loader. Here we set it None.
val_dataset_loader = None
val_dataset_size = 1

# Third step: create you model, here we use ResNet50
# ToDo: may be we can create a custom deep-learning network
model = torchvision.models.resnet50(pretrained=False)

# Copy the model to CUDA memory, and return it
if use_gpu:
    model = model.cuda()

# Fourth step: Create you criterion, 
# e.g. classification-torch.nn.CrossEntropyLoss; regression-torch.nn.MSELoss
# ToDo: you can define your customized loss function
# !!! Note: if you use CrossEntropyLoss as criterion, you needn't (and shouldn't) 
# set a softmax lay at the last of you model
criterion = torch.nn.CrossEntropyLoss()
if use_gpu:
    criterion = criterion.cuda()

# Fifth step: Create you optimizer
# ToDo: you can set different parameters for different strategy
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.01)

# Sixth step: Now, you get dataset_loader, model, criterion and optimizer, 
# then you can train your model

# define epochs you want to train
epochs = 10
# get steps per epoch
steps_per_epoch = len(image_loader)

for epoch in range(epochs):
    # ToDo: you can write you custom code to show the training process
    print(f'Epoch {epochs:02d} / {epoch:02d}')
    print('-'*30)
    # One epoch: Train data and valid validation dataset if it is existed
    # You may set some variable to record result, e.g. lossing value and accuracy.
    train_loss, val_loss, val_accuracy = 0.0, 0.0, 0.0

    # Training phase
    for step, (input_imgs, labels) in enumerate(image_loader):
        # show current step count in an epoch
        print(f"\tstep {steps_per_epoch}/{step+1}\r")
        if use_gpu:
            input_imgs = input_imgs.cuda()
            labels = labels.cuda()
        # The critical 5 steps of train
        optimizer.zero_grad()
        outputs = model(input_imgs)
        # criterion(outputs, labels) is the mean loss of this batch
        step_loss = criterion(outputs, labels)
        # lossing value back propagaton
        step_loss.backward()
        # update parameters in model
        optimizer.step()

        train_loss += step_loss
    train_loss /= steps_per_epoch
    print(f"train loss: {train_loss}")

    # Validation phase
    if val_dataset_loader is not None:
        print('begin to validation process ...')
        with torch.no_grad():
            for input_imgs, labels in val_dataset_loader:
                prediction = model(input_imgs)
                val_step_loss = criterion(prediction, labels)
                val_loss += val_step_loss
                val_accuracy += (prediction.max(dim=1)[1]==labels).sum().item()
            val_loss /= len(val_dataset_loader)
            val_accuracy = float(val_accuracy)/val_dataset_size
        print(f'val loss: {val_loss}, val accuracy: {val_accuracy}')

# Congratulations, you get an trained model


