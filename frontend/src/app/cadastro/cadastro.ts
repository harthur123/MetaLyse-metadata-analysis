import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';

// Angular Material
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-cadastro',
  standalone: true,
  imports: [
    FormsModule, MatCardModule, MatInputModule,
    MatFormFieldModule, MatButtonModule,
    RouterLink, HttpClientModule
  ],
  templateUrl: './cadastro.html',
  styleUrls: ['./cadastro.css']
})
export class Cadastro {
  username = '';
  email = '';
  password = '';

  constructor(private http: HttpClient, private router: Router) {}

  onCadastro() {
    const usuario = { username: this.username, email: this.email, password: this.password };

    this.http.post('http://127.0.0.1:5000/api/register', usuario)
      .subscribe({
        next: () => {
          alert('Cadastro realizado com sucesso!');
          this.router.navigate(['/login']);
        },
        error: (err) => alert(err.error?.message || 'Erro ao cadastrar.')
      });
  }
}
