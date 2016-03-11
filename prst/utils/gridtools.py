"""
GRIDTOOLS



Functions in MRST:
  checkGrid             - Undocumented utility function
  compareGrids          - Determine if two grid structures are the same.
  connectedCells        - Compute connected components of grid cell subsets.
  findEnclosingCell     - Find cells with closest centroid (in Euclidian norm) in a 2D grid.
  getCellNoFaces        - Get a list over all half faces, accounting for possible NNC
  getConnectivityMatrix - Derive global, undirected connectivity matrix from neighbourship relation.
  getNeighbourship      - Retrieve neighbourship relation ("graph") from grid
  gridAddHelpers        - Add helpers to existing grid structure for cleaner code structure.
  gridCellFaces         - Find faces corresponding to a set of cells
  gridCellNo            - Construct map from half-faces to cells or cell subset
  gridCellNodes         - Extract nodes per cell in a particular set of cells
  gridFaceNodes         - Find nodes corresponding to a set of faces
  gridLogicalIndices    - Given grid G and optional subset of cells, find logical indices.
  indirectionSub        - Index map of the type G.cells.facePos, G.faces.nodePos...
  makePlanarGrid        - Construct 2D surface grid from faces of 3D grid.
  neighboursByNodes     - Derive neighbourship from common node (vertex) relationship
  removeNodes           - Undocumented utility function
  sampleFromBox         - Sample from data on a uniform Cartesian grid that covers the bounding box
  sortedges             - SORTEDGES(E, POS) sorts the edges given by rows in E.
  sortGrid              - Permute nodes, faces and cells to sorted form
  transform3Dto2Dgrid   - Transforms a 3D grid into a 2D grid.
  translateGrid         - Move all grid coordinates according to particular translation
  triangulateFaces      - Split face f in grid G into subfaces.
  volumeByGaussGreens   - Compute cell volume by means of Gauss-Greens' formula

Functions in PRST:
  getNeighborship       - Retrieve neighborship relation ("graph") from grid
"""
__all__ = ["getNeighborship"]

import numpy as np

def getNeighborship(G, kind="Geometrical", incBdry=False, nargout=1):
    """
    Retrieve neighborship relation ("graph") from grid.

    Synopsis:
        N, isnnc = getNeighborship(G, kind)

    Arguments:
        G (Grid):
            PRST grid object.

        kind (str):
            What kind of neighborship relation to extract. String. The
            following options are supported:

                - "Geometrical"
                    Extract geometrical neighborship relations. The geometric
                    connections correspond to physical, geometric interfaces
                    are are the ones listed in `G.faces.neighbors`.

                - "Topological"
                    Extract topological neighborship relations. In addition to
                    the geometrical relations  of "Geometrical" these possibly
                    include non-neighboring connections resulting from
                    pinch-out processing or explicit NNC lists in an ECLIPSE
                    input deck.

                    Additional connections will only be defined if the grid `G`
                    contains an `nnc` sub-structure.

        incBdry (bool):
            Flag to indicate whether or not to include boundary connections. A
            boundary connection is a connection in which one of the connecting
            cells is the outside (i.e., cell zero). Boolean. Default: False (Do
            NOT include boundary connections.)

        nargout (int):
            Set to 2 to return both N and isnnc. Default: Return only N.

    Returns:
        N (ndarray[int]):
            Neighborshop relation. An (m, 2)-shaped array of cell indices that
            form the connections--geometrical or otherwise. This array has
            similar interpretation to the field `G.faces.neighbors`, but may
            contain additional connections if kind="Topological".

        isnnc (ndarray[bool]):
            An (m, 1)-shaped boolean array indicating whether or not the
            corresponding connection (row) of N is a geometrical connection
            (i.e., a geometric interface from the grid `G`).

            Specifically, isnnc[i,0] is True if N[i,:] comes from a
            non-neighboring (i.e., non-geometrical) connection.

    Note:
        If the neighborship relation is later to be used to compute the graph
        adjacency matrix using function `getConnectivityMatrix`, then `incBdry`
        must be False.

    See also:
        processGRDECL (MRST), processPINCH (MRST), getConnectivityMatrix (MRST)
    """
    # Geometric neighborship (default)
    N = G.faces.neighbors

    if not incBdry:
        # Exclude boundary connections
        N = N[np.all(N != -1, axis=1), :]

    if nargout >= 2:
        isnnc = np.zeros((N.shape[0], 1), dtype=bool)

    if kind=="Topological" and hasattr(G, "nnc") and hasattr(G.nnc, "cells"):
        assert G.nnc.cells.shape[1] == 2
        N = np.vstack((N, G.nnc.cells))

    if nargout >= 2:
        try:
            isnnc = np.vstack((isnnc, np.ones((G.nnc.cells.shape[0], 1), 1)))
        except AttributeError:
            pass
        return N, isnnc
    else:
        return N
