import torch
import torch.nn as nn

X = torch.tensor([
    [-0.8, -0.8],
    [-0.8, +0.8],
    [+0.8, -0.8],
    [+0.8, +0.8],
], dtype=torch.float32)
Y = torch.tensor([0.0, 1.0, 1.0, 0.0])


class XORNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.raw_W = nn.Parameter(torch.randn(2, 2))
        self.raw_b = nn.Parameter(torch.randn(2))
        self.raw_v = nn.Parameter(torch.randn(2))
        self.raw_bo = nn.Parameter(torch.randn(()))

    def actual_params(self):
        """
        Since stochastic requires param to be between -1 and 1, apply
        tanh on raw parameters
        """
        return {
            "W": torch.tanh(self.raw_W),
            "b": torch.tanh(self.raw_b),
            "v": torch.tanh(self.raw_v),
            "b_o": torch.tanh(self.raw_bo),
        }

    def forward(self, x):
        p = self.actual_params()

        h = torch.tanh(4.0 * (x @ p["W"].T + p["b"]) / 4.0)
        s = (h * p["v"]).sum(dim=-1) + p["b_o"]

        # Divide by 4 to model stochastic circuit
        s = s / 4.0

        return s

def print_params(model):
    p = model.actual_params()
    for k, v in p.items():
        print(f"  {k} =\n{v.detach().cpu().numpy()}")

def train(steps=3000, lr=0.01, seed=0):
    torch.manual_seed(seed)
    model = XORNet()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.BCEWithLogitsLoss()

    for _ in range(steps):
        opt.zero_grad()
        s = model(X)
        loss = loss_fn(8.0 * s, Y)
        loss.backward()
        opt.step()

    with torch.no_grad():
        s = model(X)
        pred = (s > 0).float()
        acc = (pred == Y).float().mean().item()
        final_loss = loss_fn(8.0 * s, Y).item()

    return model, acc, final_loss, s.detach().numpy()

if __name__ == "__main__":
    model, acc, loss, scores = train()

    print(f"acc: {acc}")
    print(f"loss: {loss}")
    print(f"scores: {scores}")
    print_params(model)
