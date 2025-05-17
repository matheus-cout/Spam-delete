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
    rl.question('Qual é o tamanho da senha? ', (tamanhoStr) => {const tamanho = parseInt(tamanhoStr);

    if (isNaN(tamanho) || tamanho < 4) {
        console.log('Por favor, digite um número válido maior que 3.');
        return rl.close();
    }

    rl.question('Incluir maiúsculas? (s/n) ', (m) => {
        rl.question('Incluir minúsculas? (s/n) ', (mi) => {
            rl.question('Incluir números? (s/n) ', (n) => {
                rl.question('Incluir símbolos? (s/n) ', (s) => {
                    
                
        }

    }
}