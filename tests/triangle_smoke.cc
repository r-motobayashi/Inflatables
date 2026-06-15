#include <MeshFEM/Triangulate.h>

#include <array>
#include <cmath>
#include <iostream>
#include <vector>

int main() {
    std::vector<std::array<double, 2>> pts;
    std::vector<std::pair<size_t, size_t>> edges;

    const size_t n = 20;
    for (size_t i = 0; i < n; ++i) {
        const double theta = (2.0 * 3.14159265358979323846 * i) / n;
        pts.push_back({{std::cos(theta), std::sin(theta)}});
        edges.emplace_back(i, (i + 1) % n);
    }

    std::vector<MeshIO::IOVertex> vertices;
    std::vector<MeshIO::IOElement> triangles;
    std::vector<int> pointMarkers;
    triangulatePSLG(pts, edges, std::vector<std::array<double, 2>>(),
                    vertices, triangles, 0.01, "", &pointMarkers, nullptr);

    std::cout << vertices.size() << " " << triangles.size() << " "
              << pointMarkers.size() << std::endl;
    return 0;
}
