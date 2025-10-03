#version 330 core
in vec3 FragPos;
in vec2 UV;
in vec3 Normal;
in vec3 Color;

out vec4 color;

void main() {
    vec3 viewDir = normalize(-FragPos);
    vec3 n = normalize(Normal);

    float cosTheta = dot(viewDir, n);
    float border = 0.05;
    float edge = min(min(UV.x, 1.0 - UV.x),
            min(UV.y, 1.0 - UV.y));

    if ((cosTheta >= 0.0) && (edge >= border)) {
        color = vec4(Color, 1.0);
    } else {
        color = vec4(0.0, 0.0, 0.0, 1.0);
    }
}
