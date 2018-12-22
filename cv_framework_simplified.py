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

# Second step : Prepare images dataset
custom_transforms_list = [
    transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.2),
    transforms.Resize((224, 224), interpolation=3), 
    transforms.Pad(10, (255, 255, 255), 'constant'),
    transforms.RandomCrop((224, 224)),  
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
]
# Compose the custom transform as a Compose object
custom_transforms = transforms.Compose(custom_transforms_list)

# Load Image Dataset
image_dataset = torchvision.datasets.ImageFolder(
    root="~/data/classified_imgs",
    transform=custom_transforms, 
    target_transform=None,
    # loader = PIL.Image.open,
)

# Create an image loader for creating batch data, and speed up load processing
image_loader = torch.utils.data.DataLoader(image_dataset,batch_size=64,shuffle=True,num_workers=4,drop_last=False)

# Validation dataset loader. Here we set it None.
val_dataset_loader = None
val_dataset_size = 1

# Third step: create you model, here we use ResNet50
# ToDo: may be we can create a custom deep-learning network
model = torchvision.models.resnet50(pretrained=False)

if use_gpu:
    model = model.cuda()

# Fourth step: Create you criterion, 
criterion = torch.nn.CrossEntropyLoss()
if use_gpu:
    criterion = criterion.cuda()

# Fifth step: Create you optimizer
# ToDo: you can set different parameters for different learning strategy
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.01)

# Sixth step: Now, you get dataset_loader, model, criterion and optimizer, then you can train your model
epochs = 10
steps_per_epoch = len(image_loader)

for epoch in range(epochs):
    # ToDo: you can write you custom code to show the training process
    print(f'Epoch {epochs:02d} / {epoch:02d}')
    print('-'*30)
    
    train_loss, val_loss, val_accuracy = 0.0, 0.0, 0.0

    # Training phase
    for step, (input_imgs, labels) in enumerate(image_loader):
        print(f"\tstep {steps_per_epoch}/{step+1}\r")
        if use_gpu:
            input_imgs = input_imgs.cuda()
            labels = labels.cuda()
        # The critical 5 steps of train
        optimizer.zero_grad()
        outputs = model(input_imgs)
        step_loss = criterion(outputs, labels)
        step_loss.backward()
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

# Congratulations, you get a trained model


