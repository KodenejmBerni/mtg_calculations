#version 330

in vec2 vTexture;

out vec4 outColor;

uniform sampler2D sTexture;

void main()
{
    gl_FragColor = texture(sTexture, vTexture);
}