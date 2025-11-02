import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-definir-senha',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
  ],
  templateUrl: './definir-senha.html',
  styleUrls: ['./definir-senha.css'],
})
export class DefinirSenha {
  novaSenha = '';
  confirmarSenha = '';

  definirSenha() {
    if (this.novaSenha === this.confirmarSenha) {
      alert('Senha definida com sucesso!');
    } else {
      alert('As senhas não coincidem.');
    }
  }
}
