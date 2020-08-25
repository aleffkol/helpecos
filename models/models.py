# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time
import re
from datetime import timedelta, date, datetime



class Chamado(models.Model):
    _name = 'chamado.chamado'  # name class

    # Barra de Status

    status = fields.Selection(
        [('analise', 'Análise'), ('aberto', 'Aberto'), ('andamento', 'Andamento'), ('concluido', 'Concluído'),
         ('encerrado', 'Encerrado'), ('pendencia', 'Pendência')], string="Status", default="analise")  # ok

    # campos Informações Principais

    protocolo = fields.Char(string="Protocolo")  # ok
    protocolo_see = fields.Char(string="Protocolo SEE", required=True)  # ok
    cliente = fields.Many2one('res.partner', string="UND Escolar", required=True)  # ok
    subsidiaria = fields.Many2one('res.company', string="Subsidiária", store=True, related='cliente.company_id')  # ok
    inep = fields.Char(string='Inep', store=True, related='cliente.ref')  # ok
    gre = fields.Char(store=True, related='cliente.street2')  # ok
    responsavel = fields.Char(string='Responsável', store=True, related='cliente.responsavel')  # ok
    email = fields.Char(string='E-mail', store=True, related='cliente.email')  # ok
    telefone = fields.Char(string='E-mail', store=True, related='cliente.phone')  # ok
    celular = fields.Char(string='E-mail', store=True, related='cliente.mobile')  # ok
    contatos = fields.Text(string="Contatos", compute="soma_contatos")  # ok
    rua = fields.Char(string='E-mail', store=True, related='cliente.street')  # ok
    cidade = fields.Char(string='E-mail', store=True, related='cliente.city')  # ok
    # estado = fields.Many2one('res.country.state', store=True, related='cliente.state_id') # ok
    cep = fields.Char(string='E-mail', store=True, related='cliente.zip')  # ok
    # pais = fields.Many2one('res.country', store=True, related='cliente.country_id') # ok
    endereco = fields.Text(string='Endereço', compute="soma_endereco")  # ok
    departamento = fields.Many2one('hr.department', string="Departamento", required=True)  # ok
    categoria = fields.Many2one('os_categoria.os_categoria', string="Categoria", required=True)  # ok
    sub_categoria = fields.Many2one('os_subcategoria.os_subcategoria', string="Sub Categoria", required=True)  # ok
    sede = fields.Many2one('sede.sede', string="Sede")  # ok
    tipo = fields.Selection([('emergencial', 'Emergêncial'), ('programado', 'Programado')], string='Tipo',
                            required=True)  # ok
    problematica = fields.Text(string='Problemática', required=True)  # ok
    chamado_relacao = fields.Many2one('chamado.chamado', string="Chamado Relação")  # ok
    dt_abertura = fields.Date(string='Data Abertura', required=True)  # ok
    dt_sla_atendimento = fields.Date(string='Data SLA Atendimento')  # ok , compute="get_sla_atendimento"
    dt_sla_conclusao = fields.Date(string='Data SLA Conclusão')  # ok , compute="get_sla_conclusao"
    docs_drive = fields.Char(string='Docs Drive', required=True)  # ok

    # Campos Andamento do Chamado

    int_sla_atendimento = fields.Char(string='SLA Atendimento Dias', compute='get_int_sla_atendimento')  # ok , compute="get_int_sla_atendimento"
    int_sla_conclusao = fields.Char(string='SLA Conclusão Dias', compute='get_int_sla_conclusao')  # ok , compute="get_int_sla_conclusao"
    dt_atendimento = fields.Date(string='Data Atendimento')  # ok
    dt_conclusao = fields.Date(string='Data Conclusão')  # ok
    avaliacao = fields.Selection(
        [('muito_ruim', 'Muito Ruim'), ('ruim', 'Ruim'), ('regular', 'Regular'), ('bom', 'Bom'),
         ('muito_bom', 'Muito Bom')], string='Avaliação')  # ok
    dp_enc_prazo = fields.Selection([('sim', 'Sim'), ('nao', 'Não'), ('null', '')], string='(DEP) Encerrado no Prazo',
                                    default="null")  # ok
    sec_enc_prazo = fields.Selection([('sim', 'Sim'), ('nao', 'Não'), ('null', '')], string='(SEC) Encerrado no Prazo',
                                     default="null")  # ok
    obs_prevencao = fields.Text(string='OBS Prevenção')
    # link_capa_chamado = fields.Char(string="Capa Chamado")  # resolver
    # folha_exec = fields.Char(string="Folha Execução") # resolver
    # rel_fotografico = fields.Char(string="Relatório Fotográfico") # resolver
    # lista_itens = fields.Char(string='Lista de Itens') # resolver

    # Pré-venda

    prev_data = fields.Date(string="Data")  # ok
    prev_nome_contato = fields.Char(string='Nome Contato')  # ok
    prev_tel_contato = fields.Char(string='Telefone Contatado')  # ok
    prev_relato = fields.Text(string='Relato')  # ok

    # Listas

    compras = fields.One2many('purchase.order', 'chamado_id')  # resolver # resolver
    vendas = fields.One2many('sale.order', 'chamado_id')  # resolver # resolver
    execucoes = fields.One2many('execucao.execucao', 'chamado_id')  # resolver # resolver

    # Pós-venda

    posv_data = fields.Date(string="Data")  # ok
    posv_nome_contato = fields.Char(string='Nome Contato')  # ok
    posv_tel_contato = fields.Char(string='Telefone Contatado')  # ok
    posv_relato = fields.Text(string='Relato')  # ok

    # funções

    @api.onchange('departamento')
    def set_departamento(self):
        for rec in self:
            if rec.departamento:
                rec.categoria = ""
                rec.sub_categoria = ""

    @api.onchange('categoria')
    def set_categoria(self):
        for rec in self:
            if rec.categoria:
                rec.sub_categoria = ""

    @api.model
    def create(self, vals):  # ok
        vals['protocolo'] = self.env['ir.sequence'].next_by_code('chamado.sequence')
        result = super(Chamado, self).create(vals)
        return result

    # @api.depends('dt_sla_atendimento')
    def get_int_sla_atendimento(self):
        hoje = datetime.now().date()
        for record in self:
            if(record.dt_sla_atendimento):
                record.int_sla_atendimento = (record.dt_sla_atendimento - hoje).days

    # @api.depends('dt_sla_conclusao')
    def get_int_sla_conclusao(self):
        hoje = datetime.now().date()
        for record in self:
            if (record.dt_sla_conclusao):
                record.int_sla_conclusao = (record.dt_sla_conclusao - hoje).days

    def eferiado(self, dia):
        feriados = self.env['holiday.holiday'].search([])
        for f in feriados:
            if(dia == f.data):
                return True
        return False

    def get_dep(self):
        departamento = self.departamento.name
        if(re.search('\\bTI\\b', departamento, re.IGNORECASE)):
            return 1
        elif(re.search('\\bMAN\\b', departamento, re.IGNORECASE)):
            return 2
        return 0

    def get_sla_atendimento(self):
        self.get_sla(0)

    def get_sla_conclusao(self):
        self.get_sla(1)

    @api.onchange('dt_abertura')
    def set_sla(self):
        for rec in self:
            if rec.dt_abertura:
                self.get_sla(0)
                self.get_sla(1)
                # self.get_int_sla_atendimento()
                # self.get_int_sla_conclusao()

    @api.depends('dt_abertura')
    def get_sla(self, sla):
        dep = self.get_dep()

        cont = 0
        slas = [[3, 15], [2, 5], [5, 15]]

        amanha = ""
        for record in self:
            if(record.dt_abertura):
                amanha = record.dt_abertura + timedelta(1)

        indice_da_semana = amanha.weekday()

        while (True):
            if (self.eferiado(amanha) == False and indice_da_semana != 5 and indice_da_semana != 6):
                cont += 1
            if (cont == slas[dep][sla]):
                if(sla == 0):
                    self.dt_sla_atendimento = amanha
                elif(sla == 1):
                    self.dt_sla_conclusao = amanha
                break
            else:
                amanha = amanha + timedelta(1)
                indice_da_semana = amanha.weekday()

    def avancar(self):  # ok
        lista = ['analise', 'aberto', 'andamento', 'concluido', 'encerrado', 'pendencia']
        if (self.status != "pendencia"):
            indice = lista.index(self.status)
            self.status = lista[indice + 1]

    def voltar(self):  # ok
        lista = ['analise', 'aberto', 'andamento', 'concluido', 'encerrado', 'pendencia']
        if (self.status != "analise"):
            indice = lista.index(self.status)
            self.status = lista[indice - 1]

    def soma_contatos(self):  # ok
        for rec in self:
            if rec.contatos:
                self.contatos = str(self.telefone) + " / " + str(self.celular)

    def soma_endereco(self):  # ok
        for rec in self:
            if rec.endereco:
                self.endereco = str(self.rua) + " / " + str(self.cidade) + " / " + str(self.cep)  # + " / " + str(self.estado) + " / " + str(self.pais)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, ("%s") % (
                record.protocolo)))
        return result


class Sede(models.Model):
    _name = 'sede.sede'  # name class

    nome = fields.Char(string="Nome", required=True)  # ok
    subsidiaria = fields.Many2one('res.company', string="Subsidiária", required=True)  # ok

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, ("%s") % (
                record.nome)))
        return result


class OSSubCategoria(models.Model):
    _name = 'os_subcategoria.os_subcategoria'  # name class

    nome = fields.Char(string="Nome", required=True)  # ok
    categoria_id = fields.Many2one(comodel_name='os_categoria.os_categoria', string="Categoria", required=True)  # ok
    subsidiaria = fields.Many2one('res.company', string="Subsidiária", store=True,
                                  related='categoria_id.subsidiaria')  # ok

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, ("%s") % (
                record.nome)))
        return result


class OSCategoria(models.Model):
    _name = 'os_categoria.os_categoria'  # name class

    nome = fields.Char(string="Nome", required=True)  # ok
    subsidiaria = fields.Many2one('res.company', string="Subsidiária", required=True)  # ok
    departamento = fields.Many2one('hr.department', string="Departamento", required=True)  # ok

    subcategorias = fields.One2many('os_subcategoria.os_subcategoria', 'categoria_id', string='Sub Categorias')  # ok

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, ("%s") % (
                record.nome)))
        return result


class Holiday(models.Model):
    _name = 'holiday.holiday'

    data = fields.Date(string="Data")  # ok
    descricao = fields.Char(string='Descrição')  # ok

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, ("%s") % (
                record.data)))
        return result


class Execucao(models.Model):
    _name = 'execucao.execucao'  # name class

    nome = fields.Char(string='Título', required=True)  # ok
    hr_inicio = fields.Datetime(string="Hora Início", required=True)  # ok
    hr_termino = fields.Datetime(string="Hora Termino", required=True)  # ok
    local = fields.Char(string='Local', required=True)
    tecnicos = fields.Text(string='Técnicos', required=True)
    servico_realizado = fields.Text(string='Serviço Realizado', required=True)
    observacao = fields.Text(string='Observação')
    material_usado = fields.Text(string='Material Usado')
    possui_pendencia = fields.Boolean(string='Possui Pendência')
    pendencias = fields.Text(string='Pendências')
    custo_estimado = fields.Float(string="Custo Estimado", required=True)
    chamado_id = fields.Many2one('chamado.chamado', string="Chamado", required=True)  # ok
    subsidiaria = fields.Many2one('res.company', string="Subsidiária", store=True,
                                  related='chamado_id.subsidiaria')  # ok

    def name_get(self):  # ok
        result = []
        for record in self:
            result.append((record.id, ("%s") % (
                record.nome)))
        return result
