#version 330

in vec3 aPosition;
in vec2 aTexture;

out vec2 vTexture;

uniform mat4 rotation;

void main()
{
    vTexture = aTexture;

    gl_Position = rotation * vec4(aPosition, 1.0);
}