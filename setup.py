from setuptools import setup, find_packages

# Lendo o conteúdo do README.md para a descrição longa
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="appmodern",
    version="0.1.0",
    author="Gustavo Felipe Felix Santiago",  # Substitua pelo seu nome
    author_email="gustavosantiago1227@gmail.com",  # Substitua pelo seu email
    description="Uma biblioteca para criar aplicações visuais com Python e tecnologias web.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GustavoSantiago1227",  # Link para o seu futuro repositório GitHub
    packages=find_packages(exclude=["exemples"]), # Exclui a pasta de exemplos do pacote
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires='>=3.6',
    # A dependência chave!
    install_requires=[
        'pywebview',
    ],
    include_package_data=True,
)