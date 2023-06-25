"""Tools to convert materials representations from Pymatgen and other codes to DGLGraphs."""
from __future__ import annotations

import abc

import numpy as np

import torch
import dgl
from dgl.backend import tensor


class GraphConverter(metaclass=abc.ABCMeta):
    """Abstract base class for converters from input crystals/molecules to graphs."""

    # def __init__(
    #     self,
    #     element_types: tuple[str, ...],
    #     cutoff: float = 5.0,
    # ):

    @abc.abstractmethod
    def get_graph(
        self,
        structure,
        src_id,
        dst_id,
        images,
        lattice_matrix,
        Z,
        element_types,
        cart_coords,
    ) -> tuple[dgl.DGLGraph, list]:
        """

        Args:
            structure: Input crystals or molecule of pymatgen structure or molecule types.
            src_id: site indices for starting point of bonds.
            dst_id: site indices for destination point of bonds.
            images: the periodic image offsets for the bonds.
            lattice_matrix: lattice information of the structure.
            Z: Atomic number information of all atoms in the structure.
            element_types: Element symbols of all atoms in the structure.
            cart_coords: Cartisian coordinates of all atoms in the structure.
        Returns:
            DGLGraph object, state_attr

        """
        u, v = tensor(src_id), tensor(dst_id)
        g = dgl.graph((u, v))
        n_missing_node = len(structure) - g.num_nodes()  # isolated atoms without bonds
        g.add_nodes(n_missing_node)
        g.edata["pbc_offset"] = torch.tensor(images)
        g.edata["lattice"] = tensor(np.repeat(lattice_matrix, g.num_edges(), axis=0))
        g.ndata["attr"] = tensor(Z)
        g.ndata["node_type"] = tensor(np.hstack([[element_types.index(site.specie.symbol)] for site in structure]))
        g.ndata["pos"] = tensor(cart_coords)
        state_attr = [0.0, 0.0]
        g.edata["pbc_offshift"] = torch.matmul(tensor(images), tensor(lattice_matrix[0]))
        return g, state_attr
