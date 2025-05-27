# mobius_strip.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class MobiusStrip:
    def __init__(self, R=5, w=2, n=200):
        """
        Initialize Möbius Strip parameters and generate mesh points.
        Args:
            R (float): Radius from center to midline of strip.
            w (float): Width of the strip.
            n (int): Mesh resolution (number of points per axis).
        """
        self.R = R
        self.w = w
        self.n = n

        # Generate u and v values
        self.u = np.linspace(0, 2 * np.pi, n)
        self.v = np.linspace(-w / 2, w / 2, n)

        # Create meshgrid
        self.U, self.V = np.meshgrid(self.u, self.v)

        # Compute 3D coordinates using parametric equations
        self.X = (R + self.V * np.cos(self.U / 2)) * np.cos(self.U)
        self.Y = (R + self.V * np.cos(self.U / 2)) * np.sin(self.U)
        self.Z = self.V * np.sin(self.U / 2)

    def compute_surface_area(self):
        """
        Approximate the surface area numerically using cross product of
        partial derivatives.
        Returns:
            float: Approximate surface area.
        """
        du = 2 * np.pi / (self.n - 1)
        dv = self.w / (self.n - 1)

        # Compute partial derivatives with respect to u
        Xu = np.gradient(self.X, du, axis=1)
        Yu = np.gradient(self.Y, du, axis=1)
        Zu = np.gradient(self.Z, du, axis=1)

        # Compute partial derivatives with respect to v
        Xv = np.gradient(self.X, dv, axis=0)
        Yv = np.gradient(self.Y, dv, axis=0)
        Zv = np.gradient(self.Z, dv, axis=0)

        # Compute cross product of partial derivatives
        cross_x = Yu * Zv - Zu * Yv
        cross_y = Zu * Xv - Xu * Zv
        cross_z = Xu * Yv - Yu * Xv

        # Compute magnitude of cross product (area of tiny surface patch)
        dA = np.sqrt(cross_x**2 + cross_y**2 + cross_z**2)

        # Approximate total surface area
        surface_area = np.sum(dA) * du * dv
        return surface_area

    def compute_edge_length(self):
        """
        Approximate the total edge length numerically by summing distances
        along both boundary curves (v = -w/2 and v = w/2) of the Möbius strip.
        Returns:
            float: Approximate total edge length.
        """
        indices = [0, -1]  # v = -w/2 and v = w/2
        edge_length = 0

        for idx in indices:
            x = self.X[idx, :]
            y = self.Y[idx, :]
            z = self.Z[idx, :]

            dx = np.diff(x)
            dy = np.diff(y)
            dz = np.diff(z)

            ds = np.sqrt(dx**2 + dy**2 + dz**2)
            edge_length += np.sum(ds)

        return edge_length


    def plot(self):
        """
        Display a 3D plot of the Möbius strip surface.
        """
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(self.X, self.Y, self.Z, cmap="viridis", edgecolor='k', alpha=0.85)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title("3D Möbius Strip")
        plt.tight_layout()
        ax.view_init(elev=30, azim=60)
        plt.show()


# ========== MAIN EXECUTION ==========

if __name__ == "__main__":
    # User-defined parameters
    R = int(input("Radius from center to midline of the strip: "))     # Radius to midline
    w = int(input("Enter Width of the strip: "))                       # Strip width
    n = int(input("Enter the value of Resolution: "))                  # Resolution

    print()
    print("-----------------------------------------------------")
    print("Output")
    print("-----------------------------------------------------")
    print()

    # Initialize Möbius Strip object
    mobius = MobiusStrip(R=R, w=w, n=n)

    # Compute surface area
    surface_area = mobius.compute_surface_area()
    print(f"Approximate Surface Area: {surface_area:.4f} units²")

    # Compute edge length
    edge_length = mobius.compute_edge_length()
    print(f"Approximate Edge Length: {edge_length:.4f} units")
    print()

    # Display 3D plot
    mobius.plot()
