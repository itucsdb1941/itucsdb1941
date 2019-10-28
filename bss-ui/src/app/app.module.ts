import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FoodListComponent } from './components/food-list/food-list.component';
import { SignComponent } from './components/sign-page/sign-page.component';
import { HttpClientModule} from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { LoginPageComponent } from './components/login-page/login-page.component';
import { NewPasswordComponent } from './components/new-password/new-password.component';


@NgModule({
  declarations: [
    AppComponent,
    FoodListComponent,
    SignComponent,
    LoginPageComponent,
    NewPasswordComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
