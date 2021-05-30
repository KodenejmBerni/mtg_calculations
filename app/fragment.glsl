#version 330

in vec3 vCol;
out vec4 gl_Color;

void main()
{
    gl_Color = vec4(vCol, 1.0);
}