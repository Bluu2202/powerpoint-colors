#include <bits/stdc++.h>
using namespace std;

using Color = array<int,3>;
static const double ALPHAS[] = {0.15, 0.3, 0.5, 0.65, 0.8, 0.95};

// lookup[i][j][alpha] → int or -1 for Kill
unordered_map<int, unordered_map<int, unordered_map<double,int>>> lookup_table;

// Convert tuple to single int
inline int tuple_to_int(const Color &c) {
    return (c[0] << 16) | (c[1] << 8) | c[2];
}

// Blending function
// return pair<bool, Color> where bool=false means Kill
pair<bool, Color> blending(const Color &c1, const Color &c2, double alpha) {
    int r = lookup_table[c1[0]][c2[0]][alpha];
    int g = lookup_table[c1[1]][c2[1]][alpha];
    int b = lookup_table[c1[2]][c2[2]][alpha];
    if (r == -1 || g == -1 || b == -1) 
        return {false, {0,0,0}};
    return {true, {r,g,b}};
}

// -------------------------------------------------------------

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "Initializing lookup table...\n";

    // Build lookup table exactly the same way as Python
    for (int i = 0; i < 256; i++) {
        for (int j = 0; j < 256; j++) {
            for (double alpha : ALPHAS) {
                double newv = i * alpha + j * (1 - alpha);
                double frac = newv - floor(newv);

                if (fabs(frac - 0.5) < 1e-6)
                    lookup_table[i][j][alpha] = -1;       // Kill
                else
                    lookup_table[i][j][alpha] = int(round(newv));
            }
        }
    }

    cout << "Initializing standard colors...\n";

    vector<Color> standard_colors = {
        {255,255,255},{248,248,248},{234,234,234},{221,221,221},{192,192,192},
        {178,178,178},{150,150,150},{128,128,128},{119,119,119},{95,95,95},
        {77,77,77},{51,51,51},{41,41,41},{28,28,28},{17,17,17},{8,8,8},
        {0,0,0},{0,51,102},{51,102,153},{51,102,204},{0,51,153},{0,0,153},
        {0,0,204},{0,0,102},{0,102,102},{0,102,153},{0,153,204},{0,102,204},
        {0,51,204},{0,0,255},{51,51,255},{51,51,153},{0,128,128},{0,153,153},
        {51,204,204},{0,204,255},{0,153,255},{0,102,255},{51,102,255},
        {51,51,204},{102,102,153},{51,153,102},{0,204,153},{0,255,204},
        {0,255,255},{51,204,255},{51,153,255},{102,153,255},{102,102,255},
        {102,0,255},{102,0,204},{51,153,51},{0,204,102},{0,255,153},
        {102,255,204},{102,255,255},{102,204,255},{153,204,255},{153,153,255},
        {153,102,255},{153,51,255},{153,0,255},{0,102,0},{0,204,0},{0,255,0},
        {102,255,153},{153,255,204},{204,255,255},{204,236,255},{204,204,255},
        {204,153,255},{204,102,255},{204,0,255},{153,0,204},{0,51,0},
        {0,128,0},{51,204,51},{102,255,102},{153,255,153},{204,255,204},
        {255,204,255},{255,153,255},{255,102,255},{255,0,255},{204,0,204},
        {102,0,102},{51,102,0},{0,153,0},{102,255,51},{153,255,102},
        {204,255,153},{255,255,204},{255,204,204},{255,153,204},{255,102,204},
        {255,51,204},{204,0,153},{128,0,128},{51,51,0},{102,153,0},{153,255,51},
        {204,255,102},{255,255,153},{255,204,153},{255,153,153},{255,102,153},
        {255,51,153},{204,51,153},{153,0,153},{102,102,51},{153,204,0},
        {204,255,51},{255,255,102},{255,204,102},{255,153,102},{255,124,128},
        {255,0,102},{214,0,147},{153,51,102},{128,128,0},{204,204,0},{255,255,0},
        {255,204,0},{255,153,51},{255,102,0},{255,80,80},{204,0,102},{102,0,51},
        {153,102,51},{204,153,0},{255,153,0},{204,102,0},{255,51,0},{255,0,0},
        {204,0,0},{153,0,51},{102,51,0},{153,102,0},{204,51,0},{153,51,0},
        {153,0,0},{128,0,0},{165,0,33}
    };

    vector<int> marks(16777216, 0);

    for (auto &c : standard_colors)
        marks[tuple_to_int(c)] = -1;

    long long number_of_colors = standard_colors.size();
    vector<Color> new_colors;

    const int update_freq = 500;
    auto start = chrono::steady_clock::now();

    cout << "Code is running!\n";

    int layer = 1;
    while (true) {
        long long options = (long long)standard_colors.size() * standard_colors.size() * 6;
        long long option_count = 0;
        int percentage = 0;

        auto layer_start = chrono::steady_clock::now();

        for (auto &color : standard_colors) {
            for (auto &mix : standard_colors) {
                for (double alpha : ALPHAS) {
                    option_count++;

                    auto res = blending(color, mix, alpha);
                    if (!res.first) continue;

                    int ci = tuple_to_int(res.second);

                    if (marks[ci] == 0) {
                        marks[ci] = tuple_to_int(color);  // Storing only base is vastly smaller than Python list
                        number_of_colors++;
                        new_colors.push_back(res.second);
                        if (number_of_colors % 1000 == 0) {
                            std::cout << "[INFO] " 
                                      << number_of_colors 
                                      << " colors constructed so far.\n";
                            std::cout.flush();   // force write even when running under nohup
                        }
                        else if (number_of_colors >= 16500000) {
                            std::cout << "Color " << ci << " has been constructed, bringing the total to " << number_of_colors << "colors" << endl;
                        }
                    }

                    if (number_of_colors >= 16777216)
                        goto finish_loops;
                }
            }
        }

finish_loops:

        if (number_of_colors >= 16777216)
            break;

        cout << "Layer " << layer 
             << " completed with " << number_of_colors 
             << " colors!\n";

        standard_colors = new_colors;
        new_colors.clear();
        layer++;
    }

    // Write output JSON
    cout << "Writing methods.json...\n";
    ofstream out("methods.json");
    out << "{";

    int percent = 0;
    for (int i = 0; i < 16777216; i++) {
        out << "\"" << i << "\": " << marks[i];
        if (i != 16777215) out << ",";

        int np = int((double)i / 16777216 * 100);
        if (np >= percent + 1) {
            percent = np;
            cout << "[" << string(percent, '#') << string(100-percent, '-') << "] ";
            cout << percent << "% (" << i << "/16777216)\n";
        }
    }

    out << "}";
    out.close();

    cout << "Finished.\n";
    return 0;
}
