#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec2 aUV;
layout(location = 2) in vec3 aNormal;
layout(location = 3) in mat4 model; // instance attribute
layout(location = 7) in vec3 aColor; // instance attribute

out vec3 FragPos;
out vec2 UV;
out vec3 Normal;
out vec3 Color;

uniform mat4 projection;
uniform mat4 view;

void main() {
    FragPos = vec3(view * model * vec4(aPos, 1.0));
    UV = aUV;
    gl_Position = projection * vec4(FragPos, 1.0);
    Normal = normalize(mat3(transpose(inverse(view * model))) * aNormal);
    Color = aColor;
}
