import torch
import dgl

from torch.testing import assert_close


from matgl.layers import GraphNorm


def test_graph_norm(graph_MoS):
    s, g1, state = graph_MoS
    gn = GraphNorm(64)

    # set learnable parameters to constant values
    gn.weight.data = 2.0 * torch.ones_like(gn.weight.data)
    gn.bias.data = torch.ones_like(gn.bias.data)
    gn.mean_scale.data = 0.75 * torch.ones_like(gn.mean_scale.data)

    features = torch.randn(g1.num_nodes(), 64)
    out = features - 0.75 * torch.mean(features, dim=0)
    std = (torch.mean(out.pow(2), dim=0) + gn.eps).sqrt()
    res = gn(g1, features)
    expected = 2.0 * out / std + 1

    assert res.shape == (2, 64)
    assert_close(res, expected)

    num_nodes = g1.num_nodes()
    batched_g = dgl.batch([g1, g1])
    batched_features = torch.randn(batched_g.num_nodes(), 64)
    out = torch.empty_like(batched_features)
    std = torch.empty_like(batched_features)
    out[:num_nodes] = batched_features[:num_nodes] - 0.75 * torch.mean(batched_features[:num_nodes], dim=0)
    std[:num_nodes] = (torch.mean(out[:num_nodes].pow(2), dim=0) + gn.eps).sqrt()
    out[num_nodes:] = batched_features[num_nodes:] - 0.75 * torch.mean(batched_features[num_nodes:], dim=0)
    std[num_nodes:] = (torch.mean(out[num_nodes:].pow(2), dim=0) + gn.eps).sqrt()

    res = gn(batched_g, batched_features)
    expected = 2.0 * out / std + 1

    assert res.shape == (4, 64)
    assert_close(res, expected)
