#version 330 core

layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aInstancePos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    vec4 worldPosition = model * vec4(aPos, 1.0) + vec4(aInstancePos, 0.0);
    gl_Position = projection * view * worldPosition;
}
