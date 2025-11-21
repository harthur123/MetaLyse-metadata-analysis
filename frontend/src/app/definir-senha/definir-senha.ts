import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-definir-senha',
  standalone: true,
  imports: [
    CommonModule, FormsModule, HttpClientModule,
    MatFormFieldModule, MatInputModule,
    MatButtonModule, MatCardModule,
    MatProgressSpinnerModule,
    RouterLink

  ],
  templateUrl: './definir-senha.html',
  styleUrls: ['./definir-senha.css'],
})
export class DefinirSenha {
  private http = inject(HttpClient);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  novaSenha = '';
  confirmarSenha = '';
  token = '';

  passwordErrors: string[] = [];
  strength = 0;
  strengthColor = 'red';

  errorMsg = '';
  successMsg = '';

  constructor() {
    this.route.queryParams.subscribe(params => {
      this.token = params['token'] || '';
    });
  }

  validatePassword() {
    const pwd = this.novaSenha;
    const errors: string[] = [];

    if (pwd.length < 6)
      errors.push("A senha deve ter no mínimo 6 caracteres.");
    if (!/[A-Z]/.test(pwd))
      errors.push("A senha deve conter pelo menos uma letra maiúscula.");
    if (!/[a-z]/.test(pwd))
      errors.push("A senha deve conter pelo menos uma letra minúscula.");
    if (!/[0-9]/.test(pwd))
      errors.push("A senha deve conter pelo menos um número.");
    if (!/[!@#$%^&*(),.?\":{}|<>]/.test(pwd))
      errors.push("A senha deve conter pelo menos um caractere especial (!@#$...).");
    if (/\s/.test(pwd))
      errors.push("A senha não pode conter espaços.");

    this.passwordErrors = errors;

    let points = 0;
    if (pwd.length >= 6) points += 20;
    if (/[A-Z]/.test(pwd)) points += 20;
    if (/[a-z]/.test(pwd)) points += 20;
    if (/[0-9]/.test(pwd)) points += 20;
    if (/[!@#$%^&*(),.?\":{}|<>]/.test(pwd)) points += 20;

    this.strength = points;

    if (points <= 40) this.strengthColor = 'red';
    else if (points <= 80) this.strengthColor = 'orange';
    else this.strengthColor = 'green';
  }

  definirSenha() {
    this.errorMsg = '';
    this.successMsg = '';

    if (this.passwordErrors.length > 0) {
      this.errorMsg = 'A senha não atende aos requisitos.';
      return;
    }

    if (this.novaSenha !== this.confirmarSenha) {
      this.errorMsg = 'As senhas não coincidem.';
      return;
    }

    this.http.post('http://127.0.0.1:5000/api/auth/reset-password', {
      token: this.token,
      new_password: this.novaSenha
    }).subscribe({
      next: () => {
        this.successMsg = 'Senha redefinida com sucesso!';
        setTimeout(() => this.router.navigate(['/login']), 2000);
      },
      error: (err) =>
        this.errorMsg = err.error?.message || 'Erro ao redefinir senha.'
    });
  }
}
