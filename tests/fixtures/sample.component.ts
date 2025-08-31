import { Component, Input, Output, EventEmitter } from '@angular/core';

export interface User {
  id: number;
  name: string;
  email: string;
}

@Component({
  selector: 'app-user-card',
  template: `
    <div class="user-card" *ngIf="user">
      <h2>{{ user.name }}</h2>
      <p>{{ user.email }}</p>
      <button (click)="onEdit()">Edit</button>
    </div>
  `,
  styles: [`
    .user-card {
      border: 1px solid #ccc;
      padding: 16px;
      border-radius: 8px;
      max-width: 300px;
    }
  `]
})
export class UserCardComponent {
  @Input() user: User | null = null;
  @Output() edit = new EventEmitter<User>();

  onEdit(): void {
    if (this.user) {
      this.edit.emit(this.user);
    }
  }
}