const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function gerarsenha(tamanho, opcoes) {
    const letrasmaiusculas = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const letrasminusculas = 'abcdefghijklmnopqrstuvwxyz';  
    const numeros = '0123456789';
    const simbolos = '!@#$%^&*()_+[]{}|;:,.<>?';

    let caracteres = '';
    if (opcoes.maiusculas) caracteres += letrasmaiusculas;
    if (opcoes.letrasminusculas) caracteres += letrasminusculas;
    if (opcoes.numeros) caracteres += numeros;
    if (opcoes.simbolos) caracteres += simbolos;

    if (!caracteres) {
        return 'Erro: Nenhuma opção de caractere selecionada.';
    }

    let senha = '';
    for (let i = 0; i < tamanho; i++) {
        const index = Math.floor(Math.random() * caracteres.length);
        senha += caracteres.charAt(index);
    }

    return senha;
}

function perguntar() {
    rl.question('Qual é o tamanho da senha? ', (tamanhoStr) => {const}
}