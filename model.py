import torch
import torch.nn as nn

class EthernetFrameGenerator(nn.Module):
    def __init__(self, input_dim=64, hidden_size=128):
        super(EthernetFrameGenerator, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_size),
            nn.BatchNorm1d(hidden_size),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, hidden_size * 2),
            nn.BatchNorm1d(hidden_size * 2),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(hidden_size * 2, hidden_size * 2),
            nn.BatchNorm1d(hidden_size * 2),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(hidden_size * 2, 5),
            nn.Sigmoid()
        )

    def forward(self, z):
        return self.network(z)

def generate_frame(model, device="cuda" if torch.cuda.is_available() else "cpu"):
    model.eval()
    with torch.no_grad():
        z = torch.randn(1, 64).to(device)
        generated = model(z)
        return generated.cpu().numpy()[0]